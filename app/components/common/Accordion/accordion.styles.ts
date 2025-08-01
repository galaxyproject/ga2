import { inkLight } from "@databiosphere/findable-ui/lib/styles/common/mixins/colors";
import {
  textBodyLarge4002Lines,
  textBodyLarge500,
} from "@databiosphere/findable-ui/lib/styles/common/mixins/fonts";
import { SHADOWS } from "@databiosphere/findable-ui/lib/styles/common/constants/shadows";

import styled from "@emotion/styled";
import { Accordion as MAccordion } from "@mui/material";

export const StyledAccordion = styled(MAccordion)`
  box-shadow: ${SHADOWS["01"]} !important;
  display: grid;
  grid-column: 1 / -1;
  padding: 12px 0;

  .MuiAccordionSummary-root {
    flex-direction: row;
    min-height: 0;
    padding: 8px 20px;

    .MuiAccordionSummary-content {
      ${textBodyLarge500};
      margin: 0;
    }
  }

  .MuiAccordionDetails-root {
    ${textBodyLarge4002Lines};
    color: ${inkLight};
    margin: 0;
    padding: 0 20px 8px;

    > *:last-child {
      margin-bottom: 0;
    }
  }
` as typeof MAccordion;
