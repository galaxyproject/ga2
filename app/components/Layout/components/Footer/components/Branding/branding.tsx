import { Logo } from "@databiosphere/findable-ui/lib/components/Layout/components/Header/components/Content/components/Logo/logo";
import { ANCHOR_TARGET } from "@databiosphere/findable-ui/lib/components/Links/common/entities";
import { Brands, LargeBrand, SmallBrand } from "./branding.styles";

export const Branding = (): JSX.Element => {
  return (
    <Brands>
      <LargeBrand>
        <Logo
          alt="NIAID"
          height={24}
          link="https://www.niaid.nih.gov"
          src="/footer/niaid.svg"
          target={ANCHOR_TARGET.BLANK}
        />
      </LargeBrand>
      <LargeBrand>
        <Logo
          alt="NIH"
          height={24}
          link="https://www.nih.gov"
          src="/footer/nih.svg"
          target={ANCHOR_TARGET.BLANK}
        />
      </LargeBrand>
      <SmallBrand>
        <Logo
          alt="HHS"
          height={32}
          link="https://www.hhs.gov"
          src="/footer/hhs.svg"
          target={ANCHOR_TARGET.BLANK}
        />
      </SmallBrand>
      <SmallBrand>
        <Logo
          alt="USA.GOV"
          height={32}
          link="https://www.usa.gov"
          src="/footer/usagov.png"
          target={ANCHOR_TARGET.BLANK}
        />
      </SmallBrand>
    </Brands>
  );
};
