"use client"; // Ensure client-side rendering
import {
  FluidPaper,
  GridPaper,
} from "@databiosphere/findable-ui/lib/components/common/Paper/paper.styles";

import { GridPaperSection } from "@databiosphere/findable-ui/lib/components/common/Section/section.styles";
import { SectionContent, StyledSection } from "../PretextItem/pretextItem.styles";

import { PretextItemProps, PretextItem } from "../PretextItem/pretextItem";
import { Typography } from "@mui/material";

export const PretextData = ({ pretextItems }: { pretextItems?: PretextItemProps[] }): JSX.Element => {
  return !pretextItems ? (
    <></>
  ) : (
    <FluidPaper>
      <GridPaper>
        <GridPaperSection> Pretext Data</GridPaperSection>
        {pretextItems.length === 0 ? (
          <StyledSection>
            <SectionContent>
              <Typography variant="h6">
                No Pretext Data found
              </Typography>
            </SectionContent>
          </StyledSection>
        ) : (
          pretextItems.map((data, index) => (
            <PretextItem key={index} pretextItem={data} />
          ))
        )}
      </GridPaper>
    </FluidPaper>
  );
};
