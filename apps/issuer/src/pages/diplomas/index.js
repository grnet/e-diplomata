import React, { useEffect, useState, useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import Button from "@digigov/ui/core/Button";
import ServiceBadge from "@digigov/ui/core/ServiceBadge";
import GovGRFooter from "@digigov/ui/govgr/Footer";
import GovGRLogo from "@digigov/ui/govgr/Logo";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import Typography from "@material-ui/core/Typography";
import Link from "next/link";
import { useResource } from "@digigov/ui/api";
import BasicLayout, {
  Bottom,
  Content,
  Main,
  Top,
} from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import ComboBox from "issuer/components/comboBox";
/* import Pagination from "@material-ui/lab/Pagination"; */
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import SearchBar from "issuer/components/searchBar";
import { debounce } from "lodash";

const useStyles = makeStyles(
  {
    top: { minHeight: "75px" },
    main: {},
    side: {},
  },
  { name: "MuiSite" }
);

export default function Diplomas() {
  const router = useRouter();
  const [diplomas, setDiplomas] = useState([]);
  /* const [dataset, setDataset] = useState([]); */
  const [searchForm, setSearchForm] = useState({
    limit: 10,
  });

  const styles = useStyles();
  const { data: datasets } = useResource("datasets");
  const { data, fetch, ...rest } = useResourceMany("diplomas", searchForm);
  console.log(data);

  const delayedSearch = useCallback(
    debounce(
      (value) =>
        setSearchForm((searchForm) => ({ ...searchForm, search: value })),
      1500
    ),
    []
  );

  async function handleInput(value) {
    console.log(value);
    await delayedSearch(value);
  }

  function handleChangeDegree({ value }) {
    console.log("value from hanldeDe is ", value);
    setSearchForm((searchForm) => ({ ...searchForm, degree: value }));
  }

  useEffect(() => {
    setDiplomas(data);
  }, [data]);

  /*  useEffect(() => {
    setDataset(datasets);
  }, [datasets]); */

  useEffect(() => {
    fetch();
  }, [searchForm]);

  const createDeploma = function () {
    router.push("/diplomas/create");
  };

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
            <PageTitleHeading>Diplomas Page</PageTitleHeading>
          </PageTitle>
          <Paragraph>Seacrh form</Paragraph>
          <SearchBar onChange={handleInput} value={searchForm.search} />
          {datasets && (
            <ComboBox
              value={searchForm.degree}
              options={datasets.degree}
              onChange={handleChangeDegree}
              variant="standard"
            ></ComboBox>
          )}

          <Button onClick={createDeploma}>Δημιουργία αιτήματος</Button>
          <List>
            {diplomas &&
              diplomas.map((row, index) => (
                <div key={index}>
                  <DiplomaItem {...row} />
                  {index + 1 <= diplomas.length && <Divider />}
                </div>
              ))}
          </List>
          {/* <Pagination
            className={styles.page}
            count={getPageTotal()}
            color="primary"
            size="large"
            page={page.noPage}
            onChange={handlePageChange}
          /> */}
        </Main>
      </Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
}

export function DiplomaItem(props) {
  const url = `/diplomas/${props.id}`;
  const classes = useStyles();

  return (
    <Link href={url}>
      <ListItem button alignItems="flex-start">
        <ListItemText
          secondary={
            <Typography variant="body2" color="textPrimary">
              Όνομα:{" "}
              <>
                <strong>{props.userName}</strong> |{" "}
              </>
              Τίτλος Σπουδών:{" "}
              <>
                <strong>{props.degree}</strong> |{" "}
              </>
              Τμήμα/Σχολή:{" "}
              <>
                <strong>{props.school}</strong> |{" "}
              </>
              Έτος:{" "}
              <>
                <strong>{props.year}</strong> |{" "}
              </>
              Status:{" "}
              <>
                <strong>{props.status}</strong> |{" "}
              </>
            </Typography>
          }
        />
      </ListItem>
    </Link>
  );
}
