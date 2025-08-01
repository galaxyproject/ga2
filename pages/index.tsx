import { GetStaticProps } from "next";
import { StyledMain } from "../app/components/Layout/components/Main/main.styles";

export const Home = (): JSX.Element => {
  return <></>;
};

export const getStaticProps: GetStaticProps = async () => {
  return {
    props: {
      pageTitle: "Genome Ark Analytics",
      themeOptions: {
        palette: {
          palette: { background: { default: "#FAFBFB" } }, // SMOKE_LIGHTEST
        },
      },
    },
  };
};

export default Home;

Home.Main = StyledMain;
