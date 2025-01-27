import { Dot } from "@databiosphere/findable-ui/lib/components/common/Dot/dot";
import { smokeMain } from "@databiosphere/findable-ui/lib/styles/common/mixins/colors";
import { css } from "@emotion/react";
import styled from "@emotion/styled";
import { ButtonBase as MButtonBase } from "@mui/material";

interface Props {
  isActive: boolean;
}

export const Bullets = styled.div`
  display: flex;
  justify-content: center;
`;

export const Bullet = styled(MButtonBase)`
  padding: 4px;
`;

export const StyledDot = styled(Dot, {
  shouldForwardProp: (props) => props !== "isActive",
})<Props>`
  background-color: ${smokeMain};
  height: 6px;
  width: 6px;

  ${({ isActive }) =>
    isActive &&
    css`
      background-color: #fc5e60;
    `}
`;
