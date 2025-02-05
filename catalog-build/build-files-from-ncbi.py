from catalog_build import build_files

ASSEMBLIES_PATH = "catalog-build/source/assemblies.yml"

UCSC_ASSEMBLIES_URL = "https://hgdownload.soe.ucsc.edu/hubs/BRC/assemblyList.json" # TODO ??

GENOMES_OUTPUT_PATH = "catalog-build/source/genomes-from-ncbi.tsv"

TAXONOMIC_GROUPS_BY_TAXONOMY_ID = {
  40674: "Mammalia",
  8782: "Aves",
  8457: "Sauropsida",
  8292: "Amphibia",
  7898: "Fish",
  7777: "Fish",
  1476529: "Fish",
}

TOLIDS_BY_TAXONOMY_ID = {
  40674: "m",
  8782: "b",
  8504: "r",
  8459: "r",
  1294634: "r",
  8292: "a",
  7898: "f",
}

if __name__ == "__main__":
  build_files(ASSEMBLIES_PATH, GENOMES_OUTPUT_PATH, UCSC_ASSEMBLIES_URL, {
    "taxonomicGroup": TAXONOMIC_GROUPS_BY_TAXONOMY_ID,
    "tolId": TOLIDS_BY_TAXONOMY_ID,
  })
