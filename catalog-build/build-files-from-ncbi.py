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

OBJECT_ASSEMBLY_DATA_PATH = "catalog-build/source/jetstream_assembly_data.tsv"
# File with a list of files that are in the expected folder but which we don't want to look at
#OBJECT_ASSEMBLY_DATA_EXCLUDED_PATH = None
OBJECT_ASSEMBLY_DATA_EXCLUDED_PATH = "catalog-build/source/skipped/jetstream_assembly_data_excluded.tsv"
# Files in the expected folder, not remove by the exclude format, that doesn't match the expected storage structure 
#OBJECT_ASSEMBLY_DATA_SKIPPED_PATH = None
OBJECT_ASSEMBLY_DATA_SKIPPED_PATH = "catalog-build/source/skipped/jetstream_assembly_data_skipped.tsv"


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


def fetch_object_storage_file_list(
  output_file,
  output_file_skipped=None,
  output_file_excluded=None,
  parts_header=None,
  parts_extract=None,
  regex_include=None,
  regex_exclude=None,
  endpoint="https://js2.jetstream-cloud.org:8001",
  bucket_name="genomeark",
  prefix="species"
):
    """
    Fetches a list of files from an S3-compatible object storage bucket, applies optional inclusion and exclusion regex filters,
    and writes the results to output files. Files can be categorized as saved, skipped, or excluded based on the provided filters.

    Args:
      output_file (str): Path to the output file where the list of selected files will be written.
      output_file_skipped (str, optional): Path to the file where skipped files (not matching include regex) will be written.
      output_file_excluded (str, optional): Path to the file where excluded files (matching exclude regex) will be written.
      parts_header (list of str, optional): Header fields to write at the top of the output file.
      parts_extract (str, optional): Regular expression pattern to extract parts from the file key for output columns.
      regex_include (str, optional): Regular expression pattern; only files matching this pattern are included.
      regex_exclude (str, optional): Regular expression pattern; files matching this pattern are excluded.
      endpoint (str, optional): S3 endpoint URL. Defaults to Jetstream Cloud public endpoint.
      bucket_name (str, optional): Name of the S3 bucket to query. Defaults to "genomeark".
      prefix (str, optional): Prefix within the bucket to filter objects. Defaults to "species".

    Writes:
      - output_file: Tab-delimited file with selected files and extracted parts (if applicable).
      - output_file_skipped: Tab-delimited file with skipped files (if specified).
      - output_file_excluded: Tab-delimited file with excluded files (if specified).

    Logs:
      Summary of total, saved, excluded, and skipped files.

    Note:
      Requires `boto3`, `botocore`, and `re` modules.
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
      writer.write(f"##Exclude regex: {regex_exclude}")
      writer.write(f"\n##Include regex: {regex_include}")
      if parts_header is not None:
        writer.write("\n#" + "\t".join(parts_header + ["path", "extension"]))
      else:
        writer.write("\n#File\textension")
      skipped_writer.write(f"#Exclude regex: {regex_exclude}")
      skipped_writer.write("\n#File\textension")
      excluded_writer.write(f"#Exclude regex: {regex_exclude}")
      excluded_writer.write("\n#File\textension")
      # Iterate through each page of results
      # Filter file in the following order
      #  1 - files not matching include regex
      #  2 - files matching exclude regex
      #  3 - files where we can't extract the different parts of interest
      for page in pages:
        for obj in page.get('Contents', []):
          object_file = obj['Key']
          counter_total += 1
          # 1 - Filter file not matching to include regex
          if regex_include is not None and not re.search(regex_include, object_file):
            skipped_writer.write(f"\n" + object_file + "\t" + extract_extension(object_file.split("/")[-1]))
            counter_skipped += 1
            continue
          # 2 - Filter file matchin exclude regex pattern
          if regex_exclude is not None and re.search(regex_exclude, object_file):
            excluded_writer.write(f"\n" + object_file + "\t" + extract_extension(object_file.split("/")[-1]))
            counter_excluded += 1
            continue
          # 3 - Try to match the object_file to the expected parts (strict)
          if parts_extract is None:
            writer.write(f"\n{object_file}")
            continue
          else:
            parts = re.match(parts_extract, object_file) 
            if parts:
              writer.write("\n" + "\t".join(map(lambda x: x or "", parts.groups())) +"\t" +  object_file + "\t" + extract_extension(object_file))
              counter_save += 1
              continue
          # Files not matching any of our regex
          skipped_writer.write(f"\n" + object_file + "\t" + extract_extension(object_file.split("/")[-1]))
          counter_skipped += 1
    logging.info(f"Total files: {counter_total}, Saved: {counter_save}, excluded: {counter_excluded}, skipped: {counter_skipped}")
    

def build_ncbi_data():
    # Update assemblies list
    update_assemblies_file(UCSC_ASSEMBLIES_SET_URL, ASSEMBLIES_PATH)
    # Get a start list of raw data files from Jetstream2 object storage
    logging.info("Parsing genomic raw data files from object storage")
    fetch_object_storage_file_list(
      OBJECT_GENOMIC_DATA_PATH,
      OBJECT_GENOMIC_DATA_SKIPPED_PATH,
      OBJECT_GENOMIC_DATA_EXCLUDED_PATH,
      ["sciName", "ToLID", "platform", "sub_path", "file"],
      r"species\/([A-Za-z]+_[A-Za-z_]+)\/([a-zA-Z0-9]+)\/genomic_data\/(?:(.+?)\/)?(.+\/)?([^\/]+)$",
      regex_include=r"^species/[A-Za-z_]+/[A-Za-z0-9]+/genomic_data/.+(cram$|cram\.crai$|fastq$|bam$|bam\.pbi$|fastq\.gz$|\.fq\.gz$|\.fq\.gz\.fai$|fastqsanger\.gz$|pod5$|pod5\.tar$|xmap$|fast5$|sam$|cmap$|cmap\.gz$)",
      regex_exclude=None)

    # Get a start list of assemblies from Jetstream2 object storage
    logging.info("Parsing assembly files from object storage")
    fetch_object_storage_file_list(
      OBJECT_ASSEMBLY_DATA_PATH,
      OBJECT_ASSEMBLY_DATA_SKIPPED_PATH,
      OBJECT_ASSEMBLY_DATA_EXCLUDED_PATH,
      ["sciName", "ToLID", "assembly", "sub_path" "file"],
      r"species\/([A-Za-z]+_[A-Za-z_]+)\/([a-zA-Z0-9]+)\/(assembly_[A-Za-z_]*)\/(?:(.+?)\/)?(.+\/)?([^\/]+)$",
      regex_include=r"^species/[A-Za-z_]+/[A-Za-z0-9]+/assembly_[A-Za-z_]*/.+(fasta$|fa$|fasta\.gz$|fa\.gz$)",
      regex_exclude="intermediates")

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
