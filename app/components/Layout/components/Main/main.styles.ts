import { Main as DXMain } from "@databiosphere/findable-ui/lib/components/Layout/components/Main/main";
import { white } from "@databiosphere/findable-ui/lib/styles/common/mixins/colors";
import styled from "@emotion/styled";

export const StyledMain = styled(DXMain)`
  flex-direction: column;
`;

export const StyledPagesMain = styled(DXMain)`
  background-color: ${white};
  flex-direction: column;
`;
