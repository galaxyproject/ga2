"use client"; // Ensure client-side rendering

import { useEffect, useState } from "react";
import { SectionContent, StyledSection } from "./pretextItem.styles";
import { Box, Button, Typography } from "@mui/material";
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import OpenInFullIcon from '@mui/icons-material/OpenInFull'; 

export interface PretextItemProps {
  image: string;
  pretext: string;
  accession: string;
}

export const PretextItem = ({ pretextItem }: { pretextItem: PretextItemProps }): JSX.Element => {
  const [imageSrc, setImageSrc] = useState<string | null>(null);
  const [loadMessage, setLoadMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchImage = async () => {
      try {
        setLoadMessage("Loading image...");
        const proxyUrl = `/api/proxy?url=${encodeURIComponent(pretextItem.image)}`;
        const response = await fetch(proxyUrl);

        if (!response.ok) {
          throw new Error(`Failed to load image: ${response.statusText}`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        setImageSrc(url);
      } catch (error) {
        setLoadMessage("Error loading image.");
        console.error("Image Load Error:", error);
      }
    };

    fetchImage();
  });

  return (
    <StyledSection>
      <SectionContent>
      <Box sx={{ position: "relative", width: "100%", display: "flex", alignItems: "center", height: 60 }}>
        <Typography variant="h6" sx={{ position: "absolute", left: "50%", transform: "translateX(-50%)" }}>
        {pretextItem.accession}
        </Typography>

        <Box sx={{ width: "100%", marginLeft: "auto", display: "flex", gap: 1, justifyContent: "flex-end" }}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => {
              if (imageSrc) {
                const newWindow = window.open("", "_blank");
                if (newWindow) {
                  newWindow.document.write(`<img src="${imageSrc}" style="width:100%; height:100%;" />`);
                  newWindow.document.title = "PrextImage for {pretextItem.accession}";
                }
              }
            }}
            style={{ marginLeft: "10px" }}
          >
            <OpenInFullIcon />
          </Button>
          <Button
            variant="contained"
            color="primary"
            href={pretextItem.pretext}
            target="_blank"
            style={{ marginLeft: "10px" }}
          >
            <CloudDownloadIcon />
          </Button>
        </Box>
      </Box>
      {imageSrc ? (
        <p>     
          <img
            src={imageSrc}
            alt="Pretext Image"
          />
        </p>
        ) : (
          <p>
            {loadMessage}
          </p>
        )}
      </SectionContent>
    </StyledSection>
  );
};
