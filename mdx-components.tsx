import {
  AlertTitle,
  AccordionDetails as MAccordionDetails,
} from "@mui/material";
import { MDXComponents } from "mdx/types";
import * as C from "./app/components";
import { Accordion } from "./app/components/common/Accordion/accordion";
import { AccordionSummary } from "./app/components/common/Accordion/components/AccordionSummary/accordionSummary";
import { Figure } from "./app/components/common/Figure/figure";

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...components,
    Accordion,
    AccordionDetails: MAccordionDetails,
    AccordionSummary,
    Alert: C.Alert,
    AlertTitle,
    Figure,
    Grid: C.Grid,
    Link: C.Link,
    RoundedPaper: C.RoundedPaper,
    a: ({ children, href }) => C.Link({ label: children, url: href ?? "" }),
  };
}
