import React, { useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import ServiceBadge from "@digigov/ui/core/ServiceBadge";
import GovGRFooter from "@digigov/ui/govgr/Footer";
import GovGRLogo from "@digigov/ui/govgr/Logo";
import BasicLayout, {
  Bottom,
  Content,
  Main,
  Top,
} from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import useAuth from "@digigov/auth";

const useStyles = makeStyles(
  {
    top: { minHeight: "75px" },
    main: {},
    side: {},
  },
  { name: "MuiSite" }
);

export default function Index() {
  const styles = useStyles();
  const auth = useAuth();
  const demoLogin = useCallback(() => {
    window.setTimeout(() => {
      window.localStorage.setItem("login-next", "/diplomas");
      window.location.href = auth.config.loginURL + "?username=test";
    }, 1);
  }, [auth.config.loginURL]);

  return (
    <BasicLayout>
      <Top className={styles.top}>
        <Header>
          <GovGRLogo />
          <HeaderTitle>
            Service name
            <ServiceBadge label="PREALPHA" />
          </HeaderTitle>
        </Header>
      </Top>
      <Content>
        <Main className={styles.main}>
          <PageTitle>
            <PageTitleHeading>Login Page</PageTitleHeading>
          </PageTitle>
          <Paragraph>Welcome text</Paragraph>
          {!auth.authenticated ? (
            <Button onClick={demoLogin}>Login</Button>
          ) : (
            <Button onClick={() => auth.logout("/")}>Logout</Button>
          )}
        </Main>
      </Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
}
