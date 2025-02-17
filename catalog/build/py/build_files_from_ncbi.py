from catalog_build import build_files

ASSEMBLIES_PATH = "catalog/source/assemblies.yml"

UCSC_ASSEMBLIES_URL = "https://hgdownload.soe.ucsc.edu/hubs/BRC/assemblyList.json"  # TODO ??

GENOMES_OUTPUT_PATH = "catalog/build/intermediate/genomes-from-ncbi.tsv"

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

TOLIDS_BY_TAXONOMY_ID = {
  40674: "m",  # Mammalia
  8782: "b",  # Aves
  32561: {  # Sauria
    "value": "r",
    "exclude": 8782  # Aves
  },
  8292: "a",  # Amphibia
  7898: "f",  # Actinopterygii
  7777: "s",  # Chondrichthyes
  7711: {  # Chordata
    "value": "k",
    "exclude": [40674, 32561, 8292, 7898, 7777]  # Mammalia, Sauria, Amphibia, Actinopterygii, Chondricthyes
  },
  10219: "k",  # Hemichordata
  7586: "e",  # Echinodermata
  6447: "x",  # Mollusca
  50557: "i",  # Insecta
}


def build_ncbi_data():
  build_files(ASSEMBLIES_PATH, GENOMES_OUTPUT_PATH, UCSC_ASSEMBLIES_URL, {
    "taxonomicGroup": TAXONOMIC_GROUPS_BY_TAXONOMY_ID,
    "tolId": TOLIDS_BY_TAXONOMY_ID,
  })


if __name__ == "__main__":
  build_ncbi_data()
