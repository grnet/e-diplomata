import React from 'react';
import { makeStyles } from "@material-ui/core";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Layout from "@diplomas/design-system/Layout";
import { Main } from "@digigov/ui/layouts/Basic";
import Grid from "@material-ui/core/Grid";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Paragraph from "@digigov/ui/typography/Paragraph";
import CallToActionButton from "@digigov/ui/core/Button/CallToAction";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
  top: { minHeight: "75px" },
  main: {},
  side: {},
});


export default function VerificationsTable({...props}) {
  const styles = useStyles();

  return (
    <Layout>
      <Main className={styles.main}>
        <Grid container direction="column" spacing={3}>
          <Grid item xs={12}>
            <PageTitle>
              <PageTitleHeading>Award verifications </PageTitleHeading>
            </PageTitle>
          </Grid>
          <Grid item xs={12}>
            <Paragraph>Welcome text</Paragraph>
          </Grid>
          <Grid item xs={12}>
            <TableContainer component={Paper}>
              <Table className={styles.table} aria-label="simple table">
                <TableHead>
                  <TableRow>
                    <TableCell>Verifier</TableCell>
                    <TableCell align="center">Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {props.data && props.data.map((row) => (
                    <TableRow key={row.id}>
                      <TableCell component="th" scope="row">
                        {row.type}
                      </TableCell>
                      <TableCell align="center">{row.status}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Grid>
          <Grid item xs={12}><CallToActionButton href="/titles">Πίσω</CallToActionButton></Grid>
        </Grid>
      </Main>
    </Layout>
  );
}