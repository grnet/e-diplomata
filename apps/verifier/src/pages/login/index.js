import React, { useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import { Main } from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import useAuth from "@digigov/auth";
import VerifierLayout from "verifier/components/VerifierLayout";
import FormBuilder, { Field } from '@digigov/form';
import { useResource } from "@digigov/ui/api";
import TextField from '@material-ui/core/TextField';
import MenuItem from '@material-ui/core/MenuItem';
const useStyles = makeStyles((theme) => ({
  main: {},
  side: {},
  formControl: {
    margin: theme.spacing(2),
    minWidth: 120,
    marginLeft: theme.spacing(0),
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}/* ,{ name: "MuiSite" } */));

export default function Index() {
  const styles = useStyles();
  const auth = useAuth();
  const [select, setSelect] = React.useState('');
  const { data } = useResource('verifier/dummy_credentials');
  const demoLogin = useCallback(async (user) => {
    window.setTimeout(() => {
      /* window.localStorage.setItem("login-next", "/shares"); */
      // window.location.href = auth.config.loginURL + "?username=test";
    }, 1);
    const response = await fetch('/api/verifier/login', {
      method: 'POST',
      body: JSON.stringify(user),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(res => res.json());
    auth.authenticate(response.token)
  }, [auth.config.loginURL]);

  return (
    <VerifierLayout>
      <Main className={styles.main}>
        <PageTitle>
          <PageTitleHeading>Login Page</PageTitleHeading>
        </PageTitle>

        {!auth.authenticated ? (
          <>
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
            {data &&
              <TextField
                select
                value={select}
                className={styles.formControl}
                onChange={(e) => {
                  const user = data[e.target.value];
                  demoLogin(user);
                }}>
                {data && data.map((verifier, index) => (
                  <MenuItem key={index} value={index}>
                    {verifier.email}
                  </MenuItem>
                ))}
              </TextField>}
          </>
        ) : (
          <Button onClick={() => auth.logout("/")}>Logout</Button>
        )}
      </Main>
    </VerifierLayout>
  );
}
