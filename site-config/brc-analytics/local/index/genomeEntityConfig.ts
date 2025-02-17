import {
  ComponentConfig,
  ListConfig,
  SORT_DIRECTION,
} from "@databiosphere/findable-ui/lib/config/entities";
import { EXPLORE_MODE } from "@databiosphere/findable-ui/lib/hooks/useExploreMode";
import { BRCDataCatalogGenome } from "../../../../app/apis/catalog/brc-analytics-catalog/common/entities";
import {
  getGenomeId,
  getGenomeTitle,
} from "../../../../app/apis/catalog/brc-analytics-catalog/common/utils";
import * as C from "../../../../app/components";
import * as V from "../../../../app/viewModelBuilders/catalog/brc-analytics-catalog/common/viewModelBuilders";
import { BRCEntityConfig } from "../../../common/entities";
import {
  BRC_DATA_CATALOG_CATEGORY_KEY,
  BRC_DATA_CATALOG_CATEGORY_LABEL,
} from "../../category";
import { mainColumn as analysisMethodsMainColumn } from "../entity/genome/analysisMethodMainColumn";
import { sideColumn as analysisMethodsSideColumn } from "../entity/genome/analysisMethodsSideColumn";
import { top as analysisMethodsTop } from "../entity/genome/analysisMethodsTop";

/**
 * Entity config object responsible to config anything related to the /assemblies route.
 */
export const genomeEntityConfig: BRCEntityConfig<BRCDataCatalogGenome> = {
  categoryGroupConfig: {
    categoryGroups: [
      {
        categoryConfigs: [
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.SPECIES,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.SPECIES,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.STRAIN,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.STRAIN,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.TAXONOMY_ID,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.TAXONOMY_ID,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.TAXONOMIC_GROUP,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.TAXONOMIC_GROUP,
          },
        ],
        label: "Organism",
      },
      {
        categoryConfigs: [
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.ACCESSION,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.ACCESSION,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.IS_REF,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.IS_REF,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.LEVEL,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.LEVEL,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.COVERAGE,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.COVERAGE,
          },
          {
            key: BRC_DATA_CATALOG_CATEGORY_KEY.ANNOTATION_STATUS,
            label: BRC_DATA_CATALOG_CATEGORY_LABEL.ANNOTATION_STATUS,
          },
        ],
        label: "Assembly",
      },
    ],
    key: "assemblies",
  },
  detail: {
    detailOverviews: [],
    staticLoad: true,
    tabs: [
      {
        label: "Choose Analysis Method",
        mainColumn: analysisMethodsMainColumn,
        route: "",
        sideColumn: analysisMethodsSideColumn,
        top: analysisMethodsTop,
      },
    ],
  },
  exploreMode: EXPLORE_MODE.CS_FETCH_CS_FILTERING,
  explorerTitle: "Assemblies",
  getId: getGenomeId,
  getTitle: getGenomeTitle,
  label: "Assemblies",
  list: {
    columns: [
      {
        componentConfig: {
          component: C.AnalyzeGenome,
          viewBuilder: V.buildAnalyzeGenome,
        } as ComponentConfig<typeof C.AnalyzeGenome, BRCDataCatalogGenome>,
        enableSorting: false,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.ANALYZE_GENOME,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.ANALYZE_GENOME,
        width: "auto",
      },
      {
        columnPinned: true,
        componentConfig: {
          component: C.Link,
          viewBuilder: V.buildAccession,
        } as ComponentConfig<typeof C.Link, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.ACCESSION,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.ACCESSION,
        width: { max: "1fr", min: "164px" },
      },
      {
        componentConfig: {
          component: C.Link,
          viewBuilder: V.buildGenomeSpecies,
        } as ComponentConfig<typeof C.Link, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.SPECIES,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.SPECIES,
        width: { max: "1fr", min: "164px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildStrain,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.STRAIN,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.STRAIN,
        width: { max: "0.5fr", min: "100px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildTaxonomyId,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.TAXONOMY_ID,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.TAXONOMY_ID,
        width: { max: "0.5fr", min: "100px" },
      },
      {
        componentConfig: {
          component: C.NTagCell,
          viewBuilder: V.buildTaxonomicGroup,
        } as ComponentConfig<typeof C.NTagCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.TAXONOMIC_GROUP,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.TAXONOMIC_GROUP,
        width: { max: "0.5fr", min: "142px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildIsRef,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.IS_REF,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.IS_REF,
        width: { max: "0.5fr", min: "80px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildLevel,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.LEVEL,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.LEVEL,
        width: { max: "0.5fr", min: "142px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildChromosomes,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.CHROMOSOMES,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.CHROMOSOMES,
        width: { max: "0.5fr", min: "142px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildLength,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.LENGTH,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.LENGTH,
        width: { max: "0.5fr", min: "120px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildScaffoldCount,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.SCAFFOLD_COUNT,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.SCAFFOLD_COUNT,
        width: { max: "0.5fr", min: "80px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildScaffoldN50,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.SCAFFOLD_N50,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.SCAFFOLD_N50,
        width: { max: "0.5fr", min: "120px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildScaffoldL50,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.SCAFFOLD_L50,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.SCAFFOLD_L50,
        width: { max: "0.5fr", min: "80px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildCoverage,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.COVERAGE,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.COVERAGE,
        width: { max: "0.5fr", min: "80px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildGcPercent,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.GC_PERCENT,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.GC_PERCENT,
        width: { max: "0.5fr", min: "80px" },
      },
      {
        componentConfig: {
          component: C.BasicCell,
          viewBuilder: V.buildAnnotationStatus,
        } as ComponentConfig<typeof C.BasicCell, BRCDataCatalogGenome>,
        header: BRC_DATA_CATALOG_CATEGORY_LABEL.ANNOTATION_STATUS,
        id: BRC_DATA_CATALOG_CATEGORY_KEY.ANNOTATION_STATUS,
        width: { max: "0.5fr", min: "142px" },
      },
    ],
    tableOptions: {
      initialState: {
        columnVisibility: {},
        sorting: [
          {
            desc: SORT_DIRECTION.ASCENDING,
            id: BRC_DATA_CATALOG_CATEGORY_KEY.SPECIES,
          },
        ],
      },
    },
  } as ListConfig<BRCDataCatalogGenome>,
  listView: {
    disablePagination: true,
    enableDownload: true,
    enableTab: false,
  },
  route: "assemblies",
  staticLoadFile: "catalog/genomes.json",
};
