export enum ANALYSIS_METHOD {
  ASSEMBLY = "ASSEMBLY",
  GENOME_COMPARISONS = "GENOME_COMPARISONS",
  PROTEIN_FOLDING = "PROTEIN_FOLDING",
  REGULATION = "REGULATION",
  TRANSCRIPTOMICS = "TRANSCRIPTOMICS",
  VARIANT_CALLING = "VARIANT_CALLING",
}

export type BRCCatalog = BRCDataCatalogGenome;

export interface BRCDataCatalogGenome {
  accession: string;
  annotationStatus: string | null;
  chromosomes: number | null;
  coverage: string | null;
  gcPercent: number;
  geneModelUrl: string | null;
  isRef: string;
  length: number;
  level: string;
  ncbiTaxonomyId: string;
  scaffoldCount: number | null;
  scaffoldL50: number | null;
  scaffoldN50: number | null;
  species: string;
  speciesTaxonomyId: string;
  sra_data: RawDataCatalog[];
  strain: string | null;
  taxonomicGroup: string[];
  tolId: string | null;
  ucscBrowserUrl: string | null;
}

export interface BRCDataCatalogOrganism {
  assemblyCount: number;
  assemblyTaxonomyIds: string[];
  genomes: BRCDataCatalogGenome[];
  maxScaffoldN50: number | null;
  ncbiTaxonomyId: string;
  species: string;
  taxonomicGroup: string[];
  tolId: string | null;
}

export interface RawDataCatalog {
  accession: string;
  biosample: string;
  instrument: string;
  library_layout: string;
  library_source: string;
  library_strategy: string;
  platform: string;
  run_total_bases: number;
  sra_run_acc: string;
  sra_sample_acc: string;
  sra_study_acc: string;
  total_bases: number;
}

export interface EntitiesResponse<R> {
  hits: R[];
  pagination: EntitiesResponsePagination;
  termFacets: Record<never, never>;
}

export interface EntitiesResponsePagination {
  count: number;
  pages: number;
  size: number;
  total: number;
}

export enum WORKFLOW_ID {
  REGULATION = "https://dockstore.org/api/ga4gh/trs/v2/tools/#workflow/github.com/iwc-workflows/chipseq-pe/main/versions/v0.12",
  TRANSCRIPTOMICS = "https://dockstore.org/api/ga4gh/trs/v2/tools/#workflow/github.com/iwc-workflows/rnaseq-pe/main/versions/v0.9",
  VARIANT_CALLING = "https://dockstore.org/api/ga4gh/trs/v2/tools/#workflow/github.com/iwc-workflows/haploid-variant-calling-wgs-pe/main/versions/v0.1",
}
