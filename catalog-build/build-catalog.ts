import { parse as parseCsv } from "csv-parse/sync";
import fsp from "fs/promises";
import {
  BRCDataCatalogGenome,
  BRCDataCatalogOrganism,
} from "../app/apis/catalog/brc-analytics-catalog/common/entities";
import { SourceGenome, RawDataGenome } from "./entities";

const SOURCE_PATH_GENOMES = "catalog-build/source/genomes-from-ncbi.tsv";

const SOURCE_PATH_RAWDATA = "catalog-build/source/primary-data-ncbi.tsv";

buildCatalog();

async function buildCatalog(): Promise<void> {
  const genomes = await buildGenomes();
  const organisms = buildOrganisms(genomes);

  console.log("Genomes:", genomes.length);
  await saveJson("catalog/genomes.json", genomes);

  console.log("Organisms:", genomes.length);
  await saveJson("catalog/organisms.json", organisms);

  console.log("Done");
}

async function buildGenomes(): Promise<BRCDataCatalogGenome[]> {
  const sourceRows = await readValuesFile<SourceGenome>(SOURCE_PATH_GENOMES);
  const rawddataRows = await readValuesFile<RawDataGenome>(SOURCE_PATH_RAWDATA);

  const mappedRows = sourceRows.map((row): BRCDataCatalogGenome => {
    const tolIds = parseList(row.tolId);
    if (tolIds.length > 1)
      console.log(
        `Warning: Multiple ToLIDs found for ${row.accession} (${tolIds.join(", ")})`
      );
    return {
      accession: row.accession,
      annotationStatus: parseStringOrNull(row.annotationStatus),
      chromosomes: parseNumberOrNull(row.chromosomeCount),
      coverage: parseStringOrNull(row.coverage),
      gcPercent: parseNumber(row.gcPercent),
      geneModelUrl: parseStringOrNull(row.geneModelUrl),
      isRef: parseBoolean(row.isRef),
      length: parseNumber(row.length),
      level: row.level,
      ncbiTaxonomyId: row.taxonomyId,
      scaffoldCount: parseNumberOrNull(row.scaffoldCount),
      scaffoldL50: parseNumberOrNull(row.scaffoldL50),
      scaffoldN50: parseNumberOrNull(row.scaffoldN50),
      species: row.species,
      speciesTaxonomyId: row.speciesTaxonomyId,
      sra_data: rawddataRows.filter(
        (rawRow) => rawRow.accession === row.accession
      ),
      strain: parseStringOrNull(row.strain),
      taxonomicGroup: parseList(row.taxonomicGroup),
      tolId: tolIds[0] ?? null,
      ucscBrowserUrl: parseStringOrNull(row.ucscBrowser),
    };
  });
  return mappedRows.sort((a, b) => a.accession.localeCompare(b.accession));
}

function buildOrganisms(
  genomes: BRCDataCatalogGenome[]
): BRCDataCatalogOrganism[] {
  const organismsByTaxonomyId = new Map<string, BRCDataCatalogOrganism>();
  for (const genome of genomes) {
    organismsByTaxonomyId.set(
      genome.speciesTaxonomyId,
      buildOrganism(organismsByTaxonomyId.get(genome.speciesTaxonomyId), genome)
    );
  }
  return Array.from(organismsByTaxonomyId.values()).sort((a, b) =>
    a.ncbiTaxonomyId.localeCompare(b.ncbiTaxonomyId)
  );
}

function buildOrganism(
  organism: BRCDataCatalogOrganism | undefined,
  genome: BRCDataCatalogGenome
): BRCDataCatalogOrganism {
  return {
    assemblyCount: (organism?.assemblyCount ?? 0) + 1,
    assemblyTaxonomyIds: Array.from(
      new Set([...(organism?.assemblyTaxonomyIds ?? []), genome.ncbiTaxonomyId])
    ),
    genomes: [...(organism?.genomes ?? []), genome],
    maxScaffoldN50: getMaxDefined(organism?.maxScaffoldN50, genome.scaffoldN50),
    ncbiTaxonomyId: genome.speciesTaxonomyId,
    species: genome.species,
    taxonomicGroup: genome.taxonomicGroup,
    tolId: genome.tolId,
  };
}

/**
 * Get maximum number among two possibly-absent values, or null if both are null or undefined.
 * @param a - First value.
 * @param b - Second value.
 * @returns maximum number, or null.
 */
function getMaxDefined(
  a: number | null | undefined,
  b: number | null | undefined
): number | null {
  if (typeof a === "number") {
    if (typeof b === "number") return Math.max(a, b);
    else return a;
  } else {
    return b ?? null;
  }
}

async function readValuesFile<T>(
  filePath: string,
  delimiter = "\t"
): Promise<T[]> {
  const content = await fsp.readFile(filePath, "utf8");
  return parseCsv(content, {
    columns: true,
    delimiter,
    relax_quotes: true,
  });
}

async function saveJson(filePath: string, data: unknown): Promise<void> {
  await fsp.writeFile(filePath, JSON.stringify(data, undefined, 2) + "\n");
}

function parseList(value: string): string[] {
  return value ? value.split(",") : [];
}

function parseStringOrNull(value: string): string | null {
  return value || null;
}

function parseNumberOrNull(value: string): number | null {
  if (!value) return null;
  return parseNumber(value);
}

function parseNumber(value: string): number {
  value = value.trim();
  const n = Number(value);
  if (!value || isNaN(n))
    throw new Error(`Invalid number value: ${JSON.stringify(value)}`);
  return n;
}

function parseBoolean(value: string): string {
  return value[0].toLowerCase() === "t" ? "Yes" : "No";
}
