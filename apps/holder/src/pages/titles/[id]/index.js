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
import Link from "@digigov/ui/core/Link";

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
  const { data, fetch: refetch, invalidate } = useResource("holder/documents", id);
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
    <Layout>
      <Main className={styles.main}>
        <Grid container direction="column">
          <Grid item xs={12}>
            <PageTitle>
              <PageTitleHeading>?????????????? ????????????</PageTitleHeading>
            </PageTitle>
          </Grid>
          <Grid item xs={12}>
            <Paragraph>Welcome text</Paragraph>
          </Grid>
          <Grid item xs={12}>
            {title && (
              <SummaryList>
                <SummaryListItem>
                  <SummaryListItemKey>??????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.holder.firstName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>??????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.holder.lastName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>??????????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.fatherName}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>???????????? ??????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.title}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>?????????? ???????????? ??????????????</SummaryListItemKey>
                  <SummaryListItemValue>
                    {title.type}
                  </SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.grade}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>??????????/??????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.department}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.issuer}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>?????????????????? ????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.dean}</SummaryListItemValue>
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>??????????????????</SummaryListItemKey>
                  {title.status && (<SummaryListItemValue>{title.status}</SummaryListItemValue>)}
                </SummaryListItem>
                <SummaryListItem>
                  <SummaryListItemKey>???????????????????? ??????????????</SummaryListItemKey>
                  <SummaryListItemValue>{title.degreeDate}</SummaryListItemValue>
                </SummaryListItem>
              </SummaryList>
            )}
          </Grid>
          <Grid container direction="row">
            <Link href={document.location.href+'share'}>????????????????????????</Link>
            <Grid item xs={4}>
              {title && (title.status === "fail") && (<Button onClick={updateStatus}>Retry</Button>)}
              {title && (title.status === "pending") && (<Button>Wait..</Button>)}
              {title && (title.status === "unawarded") && (<Button onClick={updateStatus}>Share</Button>)}
              {title && title.status === "success" && (<Button onClick={goToAwards}>??????????????</Button>)}
            </Grid>
            <Grid item xs={4}></Grid>
            <Grid item xs={4} style={{ textAlign: "right" }}><CallToActionButton href="/titles">????????</CallToActionButton></Grid>
          </Grid>
        </Grid>
      </Main>
    </Layout>
  );
}
