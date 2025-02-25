import { GridPaperSection } from "@databiosphere/findable-ui/lib/components/common/Section/section.styles";

import styled from "@emotion/styled";

interface Props {
  isPreview: boolean;
}

export const StyledSection = styled(GridPaperSection)`
  flex-direction: column;
  gap: 16px;

`;

export const SectionContent = styled.div`
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;

    img {
      width: 600px;
      height: 600px;
    }
`;