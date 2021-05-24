import React, {useCallback} from "react";
import {makeStyles} from "@material-ui/core";
import PageTitle, {PageTitleHeading} from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import {Main} from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import useAuth from "@digigov/auth";
import HolderLayout from "holder/components/HolderLayout";
import FormBuilder, {Field} from '@digigov/form';

const useStyles = makeStyles(
  {
    main: {},
    side: {},
  },
  {name: "MuiSite"}
);

export default function Index() {
  const styles = useStyles();
  const auth = useAuth();
  const demoLogin = useCallback(async (user) => {
    window.setTimeout(() => {
      window.localStorage.setItem("login-next", "/titles");
      window.location.href = auth.config.loginURL + "?username=test";
    }, 1);
    const response = await fetch('/api/holder/login', {
      method: 'POST',
      body: JSON.stringify(user),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res=>res.json());
    auth.authenticate(response.token)
  }, [auth.config.loginURL]);

  return (
    <HolderLayout>
      <Main className={styles.main}>
        <PageTitle>
          <PageTitleHeading>Login Page</PageTitleHeading>
        </PageTitle>
        {!auth.authenticated ? (
          <FormBuilder fields={[
            {
              key: 'password',
              label: {
                primary: 'Password'
              },
              type: 'string',
              extra: {
                type: 'password'
              }
            },
            {
              key: 'email',
              label: {
                primary: 'Email'
              },
              type: 'string'
            },
          ]}
            onSubmit={(data) => {
              console.log(data);
              demoLogin(data);
            }}
          >
            <Field name={'email'} />
            <Field name={'password'} />
            <Button type='submit'>Login</Button>
          </FormBuilder>
        ) : (
          <Button onClick={() => auth.logout("/")}>Logout</Button>
        )}
      </Main>
    </HolderLayout>
  );
}
