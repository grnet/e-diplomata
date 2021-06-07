import React, { useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import { Main } from "@digigov/ui/layouts/Basic";
import useAuth from "@digigov/auth";
import Layout from "@diplomas/design-system/Layout";
import FormBuilder, { Field } from '@digigov/form';

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

export default function Login(props) {
    console.log(props.data);
    const styles = useStyles();
    const auth = useAuth();
    const [select, setSelect] = React.useState('');
    const demoLogin = useCallback(async (user) => {
        const response = await fetch(props.url, {
            method: 'POST',
            body: JSON.stringify(user),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json());
        auth.authenticate(response.token)
    }, [auth.config.loginURL]);

    return (
        <Layout>
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
                        {props.data &&
                            <TextField
                                select
                                value={select}
                                className={styles.formControl}
                                onChange={(e) => {
                                    const user = props.data[e.target.value];
                                    demoLogin(user);
                                }}>
                                {props.data && props.data.map((entity, index) => (
                                    <MenuItem key={index} value={index}>
                                        {props.type === "Holder" || "Verifier" ? entity.email : entity.title}
                                    </MenuItem>
                                ))}
                            </TextField>}
                    </>
                ) : (
                    <Button onClick={() => auth.logout("/")}>Logout</Button>
                )}
            </Main>
        </Layout>

    );
}
