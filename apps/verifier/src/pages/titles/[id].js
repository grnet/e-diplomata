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
import VerifierLayout from "src/components/VerifierLayout";
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

export default function Title() {
  const router = useRouter();
  const styles = useStyles();
  const [status, setStatus] = useState();
  const [title, setTitle] = useState();
  const id = router.query.id;
  const { data, fetch: refetch, invalidate } = useResource("titles", id);
  const { data: dataChanged, loaded, loading, fetch } = useResourceAction(
    "share",
    null,
    "PUT",
    status
  );

  useEffect(() => {
    setTitle(data);
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
      statusTitle: "pending"
    })
  };

  const goToAwards = function () {
    router.push("/shares/verifications");
  }

  return (
    <VerifierLayout>
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
            {title && (
              <SummaryList>
                <SummaryListItem>
                  <SummaryListItemKey>Όνομα</SummaryListItemKey>
                  <SummaryListItemValue>{title.firstName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Επώνυμο</SummaryListItemKey>
                  <SummaryListItemValue>{title.lastName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Πατρώνυμο</SummaryListItemKey>
                  <SummaryListItemValue>{title.fatherName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Τίτλος Σπουδών</SummaryListItemKey>
                  <SummaryListItemValue>{title.degree}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Είδος Τίτλου Σπουδών</SummaryListItemKey>
                  <SummaryListItemValue>
                    {title.typeOfDegree}
                  </SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Βαθμός</SummaryListItemKey>
                  <SummaryListItemValue>{title.numberOfDegree}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Τμήμα/Σχολή</SummaryListItemKey>
                  <SummaryListItemValue>{title.school}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Ίδρυμα</SummaryListItemKey>
                  <SummaryListItemValue>{title.institution}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Πρυτανική Αρχή</SummaryListItemKey>
                  <SummaryListItemValue>{title.rector}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Κατάσταση</SummaryListItemKey>
                  {title.status && (<SummaryListItemValue>{title.status}</SummaryListItemValue>)}
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>Ημερομηνία Έκδοσης</SummaryListItemKey>
                  <SummaryListItemValue>{title.year}</SummaryListItemValue>
                </SummaryListItem>
              </SummaryList>
            )}
          </Grid>
          <Grid container direction="row">
            <Grid item xs={4} ><CallToActionButton href="/titles">Πίσω</CallToActionButton></Grid>
          </Grid>
        </Grid>
      </Main>
    </VerifierLayout>
  );
}
