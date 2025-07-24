import boto3
import pandas as pd
import re

from botocore import UNSIGNED
from botocore.config import Config
from catalog_build import build_files
from contextlib import nullcontext
import logging

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
  datefmt="%Y-%m-%d %H:%M:%S"
)
UCSC_ASSEMBLIES_SET_URL = "https://hgdownload.soe.ucsc.edu/hubs/VGP/alignment/vgp.alignment.set.metaData.txt"

ASSEMBLIES_PATH = "catalog-build/source/assemblies.yml"


OBJECT_GENOMIC_DATA_PATH = "catalog-build/source/jetstream_genomic_data.tsv"
# File with a list of files that are in the expected folder but which we don't want to look at
OBJECT_GENOMIC_DATA_EXCLUDED_PATH = None
#OBJECT_GENOMIC_DATA_EXCLUDED_PATH = "catalog-build/source/skipped/jetstream_genomic_data_excluded.tsv"
# Files in the expected folder, not remove by the exclude format, that doesn't match the expected storage structure 
OBJECT_GENOMIC_DATA_SKIPPED_PATH = None
#OBJECT_GENOMIC_DATA_SKIPPED_PATH = "catalog-build/source/skipped/jetstream_genomic_data_skipped.tsv"

UCSC_ASSEMBLIES_URL = "https://hgdownload.soe.ucsc.edu/hubs/BRC/assemblyList.json" # TODO ??

GENOMES_OUTPUT_PATH = "catalog-build/source/genomes-from-ncbi.tsv"

PRIMARYDATA_OUTPUT_PATH = "catalog-build/source/primary-data-ncbi.tsv"

TAXONOMIC_GROUPS_BY_TAXONOMY_ID = {
  40674: "Mammalia",
  8782: "Aves",
  8459: "Testudines",
  8504: "Lepidosauria",
  1294634: "Crocodylia",
  8292: "Amphibia",
  7898: "Actinopterygii",
  7777: "Chondrichthyes",
  1476529: "Cyclostomata",
  7894: "Coelacanthiformes",
  7878: "Dipnomorpha",
  2682552: "Leptocardii",
  7712: "Tunicata",
  10219: "Hemichordata",
  7586: "Echinodermata",
  6447: "Mollusca",
  50557: "Insecta",
}

TAXANOMIC_LEVELS_FOR_TREE = [
    "domain",
    "realm",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "species",
]

TOLIDS_BY_TAXONOMY_ID = {
  40674: "m", # Mammalia
  8782: "b", # Aves
  32561: { # Sauria
    "value": "r",
    "exclude": 8782 # Aves
  },
  8292: "a", # Amphibia
  7898: "f", # Actinopterygii
  7777: "s", # Chondrichthyes
  7711: { # Chordata
    "value": "k",
    "exclude": [40674, 32561, 8292, 7898, 7777] # Mammalia, Sauria, Amphibia, Actinopterygii, Chondricthyes
  },
  10219: "k", # Hemichordata
  7586: "e", # Echinodermata
  6447: "x", # Mollusca
  50557: "i", # Insecta
}

TREE_OUTPUT_PATH = "catalog-build/source/ncbi-taxa-tree.json"


def update_assemblies_file(url, output):
    try:
        df = pd.read_csv(url, sep="\t")
    except Exception as e:
        print(f"Error fetching data from URL {url}: {e}")
        return

    try:
        with open(output, 'w') as writer:
            writer.write("assemblies:")
            for _, row in df.sort_values("sciName").iterrows():
                accession = row['accession']
                sci_name = row['sciName']
                writer.write(f"\n # {sci_name}\n - accession: {accession}")
    except Exception as e:
        print(f"Error writing to file {output}: {e}")


def fetch_genomic_file_list(
    output_file,
    output_file_skipped=None,
    output_file_excluded=None,
    regex_exclude=None,
    endpoint="https://js2.jetstream-cloud.org:8001",
    bucket_name="genomeark",
    prefix="species"
):
    """
    Extracts a list of genomic data files of interest from an S3-compatible bucket, 
    filtering and categorizing files based on their storage structure and optional exclusion criteria.

    This function scans all objects under the specified prefix in the bucket, 
    identifies files matching expected genomic data patterns, and writes details to an output file.
    Files excluded by a provided regex pattern are saved to a separate file, and files that do not 
    match the expected structure (but are not excluded) are saved to another file for review.

    Args:
      output_file (str): Path to the file where matched genomic data file details will be written.
      output_file_skipped (str, optional): Path to the file where files not matching expected patterns 
        (and not excluded) will be listed. If None, skipped files are discarded.
      output_file_excluded (str, optional): Path to the file where files excluded by regex will be listed.
        If None, excluded files are discarded.
      regex_exclude (str, optional): Regular expression pattern to exclude files from the main output.
        Matching files are written to the excluded file.
      endpoint (str, optional): S3 endpoint URL for bucket access. Defaults to Jetstream Cloud.
      bucket_name (str, optional): Name of the S3 bucket to scan. Defaults to "genomeark".
      prefix (str, optional): Prefix under which to search for genomic data files. Defaults to "species".

    Notes:
      - The output file contains tab-separated columns: sciName, ToLID, platform, file, path, extension.
      - Excluded and skipped files are saved with minimal information (just the path).
      - The function uses unsigned S3 access for public buckets.
      - Only files under the "/genomic_data" subdirectory are considered.
      - The function is intended for extracting raw data files of interest for downstream analysis.

    Raises:
      Any exceptions raised by boto3 or file I/O operations are propagated.
    """
    class NullWriter:
      def write(self, *_):
          pass
      def flush(self):
          pass
    # Initialize counters at the start of the function
    counter_total, counter_save, counter_skipped, counter_excluded = 0, 0, 0, 0

    # Helper function to extract file extension, handling compressed files
    def extract_extension(file):
      parts = file.split(".")
      if parts[-1] in ["gz", "zip", "tar", "tgz"]:
        if parts[-2] == "tar":
          return ".".join(parts[-3:])
        else:
          return ".".join(parts[-2:])
      return parts[-1]
    
    # Create an S3 client with unsigned access for public bucket
    session = boto3.Session()
    client = session.client(
      's3',
      endpoint_url=endpoint,
      config=Config(signature_version=UNSIGNED)
    )
    # Use paginator to iterate through all objects under 'species' prefix
    paginator = client.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=prefix)
    # Open output files for writing results, skipped, and excluded files
    with open(output_file, 'w') as writer, \
      open(output_file_skipped, 'w') if output_file_skipped else nullcontext(NullWriter()) as skipped_writer, \
      open(output_file_excluded, 'w') if output_file_excluded else nullcontext(NullWriter()) as excluded_writer:
      # Write headers to output files
      writer.write(f"#Exclude regex: {regex_exclude}\n")
      writer.write("#sciName\tToLID\tplatform\tfile\tpath\textension")
      skipped_writer.write(f"#Exclude regex: {regex_exclude}")
      excluded_writer.write(f"#Exclude regex: {regex_exclude}")
      # Iterate through each page of results
      for page in pages:
        for obj in page.get('Contents', []):
          key = obj['Key']
          counter_total += 1
          # Filter files by required substring
          if "/genomic_data/" not in key:
            continue
          # Exclude files matching the regex pattern
          if regex_exclude is not None and re.search(regex_exclude, key):
            excluded_writer.write(f"\n{key}")
            counter_excluded += 1
            continue
          # Try to match the key to the expected genomic data file pattern (strict)
          match1 = re.match(
            r"species/([A-Za-z]+_[a-z]+)/([a-z]+[A-Z][a-z]+[A-Za-z]+\d+)/genomic_data/([A-Za-z0-9_-]+)/([^/]+)$",
            key
          )
          if match1:
            sciName, tolid, platform, filename = match1.groups()
            writer.write(f"\n{sciName}\t{tolid}\t{platform}\t{filename}\t{key}\t{extract_extension(filename)}")
            counter_save += 1
            continue
          # Try to match a more permissive pattern for genomic data files
          match2 = re.match(
            r"species/([A-Za-z]+_[a-z]+)/([a-z]+[A-Z][a-z]+[A-Za-z]+\d+)/genomic_data/(.+)/([^/]+)$",
            key
          )
          if match2:
            sciName, tolid, platform, filename = match2.groups()
            writer.write(f"\n{sciName}\t{tolid}\t{platform}\t{filename}\t{key}\t{extract_extension(filename)}")
            counter_save += 1
            continue
          # If no pattern matches, write the key to the skipped file.
          counter_skipped += 1
    logging.info(f"Total files: {counter_total}, Saved: {counter_save}, excluded: {counter_excluded}, skipped: {counter_skipped}")
    

def build_ncbi_data():
    # Update assemblies list
    update_assemblies_file(UCSC_ASSEMBLIES_SET_URL, ASSEMBLIES_PATH)
    
    # Get a start list of files from Jetstream2 object storage
    fetch_genomic_file_list(
      OBJECT_GENOMIC_DATA_PATH,
      OBJECT_GENOMIC_DATA_SKIPPED_PATH,
      OBJECT_GENOMIC_DATA_EXCLUDED_PATH,
      regex_exclude=r"intermediates|scripts|transferdone|run-info|.*\.txt$|.*\.txt\.gz$|.*\.log$|.*\.log\.gz$|.*\.TXT$|.*\.tsv$|.*\.csv$|.*\.tsv\.gz$|.*\.tsv\.gz$|.*\.json\.gz$|.*\.json$|.*\.json$|.*\.md5?$|.*\.xml\.gz$|.*\.pkl$|.*\.xml$|.*\.yaml$|.*\.html$|.*\.out$|.*\.stats$|.*\.rd$|.*\.sh$|.*\.hist$|.*\.errbin$|/gc/|README|readme")

    build_files(
      ASSEMBLIES_PATH,
      GENOMES_OUTPUT_PATH,
      UCSC_ASSEMBLIES_URL,
      TREE_OUTPUT_PATH,
      TAXANOMIC_LEVELS_FOR_TREE,
      {
        "taxonomicGroup": TAXONOMIC_GROUPS_BY_TAXONOMY_ID,
        "tolId": TOLIDS_BY_TAXONOMY_ID,
      },
      primary_output_path=PRIMARYDATA_OUTPUT_PATH, extract_primary_data=True)

if __name__ == "__main__":
  build_ncbi_data()
