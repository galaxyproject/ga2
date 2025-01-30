import ky from "ky";
import { WORKFLOW_ID } from "../apis/catalog/brc-analytics-catalog/common/entities";

interface WorkflowLandingsBody {
  public: true;
  request_state: WorkflowLandingsBodyRequestState;
  workflow_id: string;
  workflow_target_type: "trs_url";
}

type WorkflowLandingsBodyRequestState = {
  [key: string]: { [key: string]: string } | string;
};

interface WorkflowLanding {
  uuid: string;
}

const WORKFLOW_LANDINGS_API_URL =
  "https://test.galaxyproject.org/api/workflow_landings";

const WORKFLOW_LANDING_URL_PREFIX =
  "https://test.galaxyproject.org/workflow_landings/";

/**
 * Get the URL of the workflow landing page for the given genome workflow.
 * @param workflowId - Value for the `workflow_id` parameter sent to the API.
 * @param referenceGenome - Genome version/assembly ID.
 * @param geneModelUrl - URL for gene model parameter sent to the API.
 * @returns workflow landing URL.
 */
export async function getWorkflowLandingUrl(
  workflowId: WORKFLOW_ID,
  referenceGenome: string,
  geneModelUrl: string | null
): Promise<string> {
  const body: WorkflowLandingsBody = {
    public: true,
    request_state: getWorkflowLandingsRequestState(
      workflowId,
      referenceGenome,
      geneModelUrl
    ),
    workflow_id: workflowId,
    workflow_target_type: "trs_url",
  };
  const res = await ky.post<WorkflowLanding>(WORKFLOW_LANDINGS_API_URL, {
    json: body,
    retry: {
      methods: ["post"],
    },
  });
  const id = (await res.json()).uuid;
  return `${WORKFLOW_LANDING_URL_PREFIX}${encodeURIComponent(id)}?public=true`;
}

function buildFastaUrl(identifier: string): string {
  const baseUrl = "https://hgdownload.soe.ucsc.edu/hubs/";
  const parts = identifier.split("_");
  const formattedPath = `${parts[0]}/${parts[1].slice(0, 3)}/${parts[1].slice(
    3,
    6
  )}/${parts[1].slice(6, 9)}/${identifier}/${identifier}.fa.gz`;
  return `${baseUrl}${formattedPath}`;
}

/**
 * Get the appropriate `request_state` object for the given workflow ID and reference genome.
 * @param workflowId - Workflow ID.
 * @param referenceGenome - Reference genome.
 * @param geneModelUrl - URL for gene model parameter.
 * @returns `request_state` value for the workflow landings request body.
 */
function getWorkflowLandingsRequestState(
  workflowId: WORKFLOW_ID,
  referenceGenome: string,
  geneModelUrl: string | null
): WorkflowLandingsBodyRequestState {
  if (workflowId === WORKFLOW_ID.VARIANT_CALLING && geneModelUrl) {
    return {
      "Annotation GTF": { ext: "gtf.gz", src: "url", url: geneModelUrl },
      "Genome fasta": {
        ext: "fasta.gz",
        src: "url",
        url: buildFastaUrl(referenceGenome),
      },
    };
  }
  return { reference_genome: referenceGenome };
}
