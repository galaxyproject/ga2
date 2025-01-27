import { smokeLightest } from "@databiosphere/findable-ui/lib/theme/common/palette";
import { GetStaticProps } from "next";
import { StyledMain } from "../app/components/Layout/components/Main/main.styles";

export const Home = (): JSX.Element => {
  return <></>;
};

export const getStaticProps: GetStaticProps = async () => {
  return {
    props: {
      pageTitle: "Genome Ark 2",
      themeOptions: {
        palette: {
          background: { default: smokeLightest },
        },
      },
    },
  };
};

export default Home;

Home.Main = StyledMain;
