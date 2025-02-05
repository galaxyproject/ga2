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

if __name__ == "__main__":
  build_files(ASSEMBLIES_PATH, GENOMES_OUTPUT_PATH, UCSC_ASSEMBLIES_URL, {
    "taxonomicGroup": TAXONOMIC_GROUPS_BY_TAXONOMY_ID,
  })
