from catalog_build import build_files
import pandas as pd

UCSC_ASSEMBLIES_SET_URL = "https://hgdownload.soe.ucsc.edu/hubs/VGP/alignment/vgp.alignment.set.metaData.txt"

ASSEMBLIES_PATH = "catalog-build/source/assemblies.yml"

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


def build_ncbi_data():
    # Update assemblies list
    update_assemblies_file(UCSC_ASSEMBLIES_SET_URL, ASSEMBLIES_PATH)
    
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
