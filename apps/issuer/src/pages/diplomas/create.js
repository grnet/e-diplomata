import React, { useCallback, useEffect, useState } from "react";
import { makeStyles } from "@material-ui/core";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import ServiceBadge from "@digigov/ui/core/ServiceBadge";
import GovGRFooter from "@digigov/ui/govgr/Footer";
import GovGRLogo from "@digigov/ui/govgr/Logo";
import BasicLayout, {
  Bottom,
  Content,
  Main,
  Top,
} from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import useAuth from "@digigov/auth";
import FormBuilder, { Field } from "@digigov/form";
import { useResourceAction } from "@digigov/ui/api";
export const fields = [
  {
    key: "degree",
    type: "string",
    required: true,
    label: {
      primary: "Τίτλος Σπουδών",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "typeOfDegree",
    type: "string",
    required: true,
    label: {
      primary: "Είδος Τίτλου Σπουδών",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "school",
    type: "string",
    required: true,
    label: {
      primary: "Τμήμα/Σχολή",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "institution",
    type: "string",
    required: true,
    label: {
      primary: "Ίδρυμα",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "status",
    type: "string",
    required: true,
    label: {
      primary: "Κατάσταση",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "userName",
    type: "string",
    required: true,
    label: {
      primary: "Ονοματεπώνυμο",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
  {
    key: "year",
    type: "string",
    required: true,
    label: {
      primary: "Ημερομηνία Έκδοσης",
    },
    layout: {
      xs: 5,
      sm: 6,
    },
  },
];

const useStyles = makeStyles(
  {
    top: { minHeight: "75px" },
    main: {},
    side: {},
  },
  { name: "MuiSite" }
);

export default function CreateDiploma() {
  const styles = useStyles();
  const [formData, setFormData] = useState();
  const { data, loaded, loading, fetch } = useResourceAction(
    "diplomas",
    null,
    "POST",
    formData
  );
  useEffect(() => {
    if (formData) {
      fetch();
    }
  }, [formData]);
  /* debugger; */
  return (
    <BasicLayout>
      <Top className={styles.top}>
        <Header>
          <GovGRLogo />
          <HeaderTitle>
            Service name
            <ServiceBadge label="PREALPHA" />
          </HeaderTitle>
        </Header>
      </Top>
      <Content>
        <Main className={styles.main}>
          <PageTitle>
            <PageTitleHeading>Login Page</PageTitleHeading>
          </PageTitle>
          <Paragraph>Welcome text</Paragraph>
          <FormBuilder
            fields={fields}
            onSubmit={(data) => {
              setFormData(data);
            }}
          >
            {fields.map((field) => (
              <Field key={field.key} name={field.key} />
            ))}

            <Button type="submit" disabled={loading}>
              Submit
            </Button>
          </FormBuilder>
        </Main>
      </Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
}
