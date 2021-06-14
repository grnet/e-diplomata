import React, {useEffect, useState} from "react";
import {Main} from "@digigov/ui/layouts/Basic";
import Header, {HeaderTitle} from "@digigov/ui/app/Header";
import {makeStyles} from "@material-ui/core";
import Button from "@digigov/ui/core/Button";
import Paragraph from "@digigov/ui/typography/Paragraph";
import PageTitle, {PageTitleHeading} from "@digigov/ui/app/PageTitle";
import CallToActionButton from "@digigov/ui/core/Button/CallToAction";
import {useRouter} from "next/router";
import {NormalText} from "@digigov/ui";
import {useResource} from "@digigov/ui/api";
import {
  SummaryList,
  SummaryListItem,
  SummaryListItemKey,
  SummaryListItemValue,
  SummaryListItemAction,
} from "@digigov/ui/core/SummaryList";
import Layout from "@diplomas/design-system/Layout";
import {useResourceAction} from "@digigov/ui/api";
import Grid from "@material-ui/core/Grid";
import FormBuilder, {Field} from "@digigov/form";

const useStyles = makeStyles(
  {
    top: {minHeight: "75px"},
    main: {},
    side: {},
  },
  {name: "MuiSite"}
);

export default function Title() {
  const router = useRouter();
  const styles = useStyles();
  const [formData, setFormData] = useState();
  const id = router.query.id;
  const {data: dataChanged, loaded, loading, fetch} = useResourceAction(
    "holder/documents",
    `${id}/shares`,
    "POST",
    formData
  );


  useEffect(() => {
    if(formData) {
      fetch();
    }
  }, [formData]);



  return (
    <Layout>
      <Main className={styles.main}>
        <Grid container direction="column">
          <Grid item xs={12}>
            <PageTitle>
              <PageTitleHeading>Διαμοιρασμός τίτλου</PageTitleHeading>
            </PageTitle>
          </Grid>

          <Grid item xs={12}>
            <FormBuilder
              onSubmit={(data) => {
                setFormData(data);
              }}
              fields={[
                {
                  key: 'verifier',
                  type: 'string',
                  label: {
                    primary: 'Verifier address'
                  }
                }
              ]}>
              <Field name={'verifier'}></Field>
              <Button type="submit" >Share</Button>
            </FormBuilder>
          </Grid>
        </Grid>
      </Main>
    </Layout>
  );
}
