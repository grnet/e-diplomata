import React, { useEffect, useState } from "react";
import { Main } from "@digigov/ui/layouts/Basic";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import { makeStyles } from "@material-ui/core";
import Button from "@digigov/ui/core/Button";
import Paragraph from "@digigov/ui/typography/Paragraph";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import CallToActionButton from "@digigov/ui/core/Button/CallToAction";
import { useRouter } from "next/router";
import { NormalText } from "@digigov/ui";
import { useResource } from "@digigov/ui/api";
import {
  SummaryList,
  SummaryListItem,
  SummaryListItemKey,
  SummaryListItemValue,
  SummaryListItemAction,
} from "@digigov/ui/core/SummaryList";
import Layout from "@diplomas/design-system/Layout";
import { useResourceAction } from "@digigov/ui/api";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles(
  {
    top: { minHeight: "75px" },
    main: {},
    side: {},
  },
  { name: "MuiSite" }
);

export default function Diploma() {
  const router = useRouter();
  const styles = useStyles();
  const [diploma, setDiploma] = useState();
  const [status, setStatus] = useState();
  const id = router.query.id;
  const { data, invalidate } = useResource("issuer/documents", id);

  useEffect(() => {
    setDiploma(data);
  }, [data]);

  const updateStatus = function () {
    setStatus({
      id: router.query.id,
      statusDiploma: "pending"
    })
  };

  const goToAwards = function () {
    router.push("/awards/verifications");
  }

  return (
    <Layout>
      <Main className={styles.main}>
        <Grid container direction="column">
          <Grid item xs={12}>
            <PageTitle>
              <PageTitleHeading>Προβολή τίτλου</PageTitleHeading>
            </PageTitle>
          </Grid>
          <Grid item xs={12}>
            <Paragraph>Welcome text</Paragraph>
          </Grid>
          <Grid item xs={12}>
            {diploma && (
              <SummaryList>
                <SummaryListItem>
                  <SummaryListItemKey>Τίτλος Σπουδών</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.title}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Είδος Τίτλου Σπουδών</SummaryListItemKey>
                  <SummaryListItemValue>
                    {diploma.type}
                  </SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Τμήμα/Σχολή</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.department}</SummaryListItemValue>
                </SummaryListItem>
              </SummaryList>
            )}
          </Grid>
          <Grid container direction="row">
            <Grid item xs={4}>
            </Grid>
            <Grid item xs={4}></Grid>
            <Grid item xs={4} style={{ textAlign: "right" }}><CallToActionButton href="/diplomas">Πίσω</CallToActionButton></Grid>
          </Grid>
        </Grid>
      </Main>
    </Layout>
  );
}
