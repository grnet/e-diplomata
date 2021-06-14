import React, { useEffect, useState } from "react";
import { Main } from "@digigov/ui/layouts/Basic";
import { makeStyles } from "@material-ui/core";
import Paragraph from "@digigov/ui/typography/Paragraph";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import CallToActionButton from "@digigov/ui/core/Button/CallToAction";
import { useRouter } from "next/router";
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
import Button from "@digigov/ui/core/Button";


const useStyles = makeStyles(
  {
    top: { minHeight: "75px" },
    main: {},
    side: {},
  },
  { name: "MuiSite" }
);

export default function DocumentById({ props }) {
  const router = useRouter();
  const styles = useStyles();
  const [document, setDocument] = useState();
  const [status, setStatus] = useState();
  const id = router.query.id;
  const { data, invalidate } = useResource(props.url, id);
  console.log("document", document);
  console.log("props", props);
  useEffect(() => {
    setDocument(data);
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
              <PageTitleHeading>{props.title}</PageTitleHeading>
            </PageTitle>
          </Grid>
          <Grid item xs={12}>
            <Paragraph>{props.content}</Paragraph>
          </Grid>
          <Grid item xs={12}>
            {props.presentation && props.presentation.fields.map((field, index) => {
              return (
                <SummaryList key={index}>
                  <SummaryListItem>
                    <SummaryListItemKey>{field.label}</SummaryListItemKey>
                    {document && <SummaryListItemValue>{document[field.key]}</SummaryListItemValue>}
                  </SummaryListItem>
                </SummaryList>

              )
            })}
          </Grid>
          <Grid container direction="row">
            {props.showButtons && <Grid item xs={4}>
              {document && (document.status === "fail") && (<Button onClick={updateStatus}>Retry</Button>)}
              {document && (document.status === "pending") && (<Button>Wait..</Button>)}
              {document && (document.status === "unawarded") && (<Button onClick={updateStatus}>Share</Button>)}
              {document && document.status === "success" && (<Button onClick={goToAwards}>Προβολή</Button>)}
            </Grid>}
            {props.showButtons && <Grid item xs={4}></Grid>}
            <Grid item xs={4} style={{ textAlign: props.showButtons=== true? "right":"left" }}><CallToActionButton href={props.href}>Πίσω</CallToActionButton></Grid>
          </Grid>
        </Grid>
      </Main>
    </Layout>
  );
}