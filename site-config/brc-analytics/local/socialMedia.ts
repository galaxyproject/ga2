import { SocialMedia } from "@databiosphere/findable-ui/lib/components/Layout/components/Header/common/entities";
import * as C from "../../../app/components";

export const SOCIALS = {
  DISCOURSE: {
    label: "Discourse",
    url: "TODO",
  },
  GITHUB: {
    label: "GitHub",
    url: "https://github.com/galaxyproject/ga2",
  },
};

export const socialMedia: SocialMedia = {
  socials: [
    {
      ...SOCIALS.DISCOURSE,
      Icon: C.DiscourseIcon,
    },
    {
      ...SOCIALS.GITHUB,
      Icon: C.GitHubIcon,
    },
  ],
};
