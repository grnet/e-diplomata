import React, { useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import { Main } from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import useAuth from "@digigov/auth";
import VerifierLayout from "verifier/components/VerifierLayout";

const useStyles = makeStyles(
  {
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
      window.localStorage.setItem("login-next", "/titles");
      window.location.href = auth.config.loginURL + "?username=test";
    }, 1);
  }, [auth.config.loginURL]);

  return (
    <VerifierLayout>
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
    </VerifierLayout>
  );
}
