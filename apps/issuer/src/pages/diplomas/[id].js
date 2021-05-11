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
import IssuerLayout from "src/components/IssuerLayout";
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
  const { data, fetch:refetch, invalidate } = useResource("diplomas", id);
  const { data: dataChanged, loaded, loading, fetch } = useResourceAction(
    "award",
    null,
    "PUT",
    status
  );
  console.log(dataChanged);
  useEffect(() => {
    setDiploma(data);
  }, [data]);

  useEffect(() => {
    if (status) {
      fetch();
    }
  }, [status]);

  useEffect(() => {
    if (loaded) {
      invalidate();
        refetch(); 
      
    }
  }, [loaded]);

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
    <IssuerLayout>
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
                  <SummaryListItemValue>{diploma.degree}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Είδος Τίτλου Σπουδών</SummaryListItemKey>
                  <SummaryListItemValue>
                    {diploma.typeOfDegree}
                  </SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Τμήμα/Σχολή</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.school}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Ίδρυμα</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.institution}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItem>
                    <SummaryListItemKey>Κατάσταση</SummaryListItemKey>
                    {diploma.status && (<SummaryListItemValue>{diploma.status}</SummaryListItemValue>)}
                  </SummaryListItem>
                  <SummaryListItemKey>Ονοματεπώνυμο</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.userName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Ημερομηνία Έκδοσης</SummaryListItemKey>
                  <SummaryListItemValue>{diploma.year}</SummaryListItemValue>
                </SummaryListItem>
              </SummaryList>
            )}
          </Grid>
          <Grid container direction="row">
            <Grid item xs={4}>
              {diploma &&  (diploma.status === "fail") && (<Button onClick={updateStatus}>Retry</Button>)}
              {diploma &&  (diploma.status === "pending") && (<Button>Wait..</Button>)}
              {diploma && (diploma.status === "unawarded") && (<Button onClick={updateStatus}>Award</Button>)}
              {diploma && diploma.status === "success" && (<Button onClick={goToAwards}>Προβολή</Button>)}
            </Grid>
            <Grid item xs={4}></Grid>
            <Grid item xs={4} style={{ textAlign: "right" }}><CallToActionButton href="/diplomas">Πίσω</CallToActionButton></Grid>
          </Grid>
        </Grid>
      </Main>
    </IssuerLayout>
  );
}
