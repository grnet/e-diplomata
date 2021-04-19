import React, { useEffect, useState } from "react";
import { Main } from "@digigov/ui/layouts/Basic";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import { makeStyles } from "@material-ui/core";
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
import GenericTemplate from "src/components/genericTemplate";

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
  const id = router.query.id;
  const { data } = useResource("diplomas", id);
  useEffect(() => {
    setDiploma(data);
  }, [data]);
  /* debugger; */
  return (
    <GenericTemplate>
      <Main className={styles.main}>
        <PageTitle>
          <PageTitleHeading>Προβολή τίτλου</PageTitleHeading>
        </PageTitle>
        <Paragraph>Welcome text</Paragraph>
        {diploma && (
          <SummaryList>
            <SummaryListItem>
              <SummaryListItemKey>Τίτλος Σπουδών</SummaryListItemKey>
              <SummaryListItemValue>{diploma.degree}</SummaryListItemValue>
              {/* <SummaryListItemAction> Αλλαγή</SummaryListItemAction> */}
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
                <SummaryListItemValue>{diploma.status}</SummaryListItemValue>
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
        <CallToActionButton href="/diplomas">Πίσω</CallToActionButton>
      </Main>
    </GenericTemplate>
  );
}
