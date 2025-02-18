export interface SourceGenome {
  accession: string;
  annotationStatus: string;
  chromosomeCount: string;
  coverage: string;
  gcPercent: string;
  geneModelUrl: string;
  isRef: string;
  length: string;
  level: string;
  scaffoldCount: string;
  scaffoldL50: string;
  scaffoldN50: string;
  species: string;
  speciesTaxonomyId: string;
  strain: string;
  taxonomicGroup: string;
  taxonomyId: string;
  tolId: string;
  ucscBrowser: string;
}

export interface RawDataGenome {
  accession: string;
  biosample: string;
  instrument: string;
  library_layout: string;
  library_source: string;
  library_strategy: string;
  platform: string;
  run_total_bases: number;
  sra_ids: string;
  sra_run_acc: string;
  sra_sample_acc: string;
  sra_study_acc: string;
  total_bases: number;
}
