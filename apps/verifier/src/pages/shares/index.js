


import React, { useEffect, useState, useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import PageTitle, { PageTitleHeading } from "@digigov/ui/app/PageTitle";
import Button from "@digigov/ui/core/Button";
import List from "@material-ui/core/List";
import Divider from "@material-ui/core/Divider";
import { useResource } from "@digigov/ui/api";
import { Main } from "@digigov/ui/layouts/Basic";
import Paragraph from "@digigov/ui/typography/Paragraph";
import { Title, NormalText } from "@digigov/ui/typography";
import ComboBox from "verifier/components/comboBox";
import Grid from "@material-ui/core/Grid";
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import SearchBar from "verifier/components/searchBar";
import { debounce } from "lodash";
import Pagination from "@material-ui/lab/Pagination";
import VerifierLayout from "verifier/components/VerifierLayout";
import SharedTitleItem from "verifier/components/SharedTitleItem";
import CallToActionButton from "@digigov/ui/core/Button/CallToAction";

const useStyles = makeStyles((theme) => ({
  top: { minHeight: "75px" },
  main: {},
  box: {
    padding: theme.spacing(4),
  },
  alignLeft: {
    margin: "auto",
    textAlign: "left",
  },
  alignRight: {
    margin: "auto",
    textAlign: "right",
  },
  banner: {
    marginBottom: theme.spacing(6),
  },
  toolkitBanner: {
    backgroundColor: theme.palette.grey["800"],
  },
  caption: {
    color: theme.palette.common.white,
  },
  image: {
    display: "block",
    width: "50%",
    margin: `${theme.spacing(4)}px auto`,
  },
  page: {
    "& > *": {
      marginTop: theme.spacing(2),
    },
  },
  title: {
    marginTop: "-9px",
  },
}));

export default function SharedTitle() {
  const router = useRouter();
  const [titles, setTitles] = useState([]);
  const [searchForm, setSearchForm] = useState({
    limit: 10,
    offset: 1,
  });

  const styles = useStyles();
/*   const { data: datasets } = useResource("datasets"); */
  const { data, fetch, ...rest } = useResourceMany("titles", searchForm);

  const delayedSearch = useCallback(
    debounce(
      (value) =>
        setSearchForm((searchForm) => ({ ...searchForm, search: value })),
      1200
    ),
    []
  );

  async function handleSearch(value) {
    await delayedSearch(value);
  }

  async function handlePageChange(event, value) {
    if (searchForm.offset !== value) {
      await setSearchForm((prevState) => ({
        ...prevState,
        offset: value,
      }));
    }
  }

  function getPageTotal() {
    return Math.ceil(rest.totalPages);
  }

  useEffect(() => {
    setTitles(data);
  }, [data]);

  useEffect(() => {
    fetch();
  }, [searchForm]);

  return (
    <VerifierLayout>
      <Main xs={12} md={12} className={styles.main}>
        <Grid container direction="column">
          <PageTitle>
            <Grid item xs={12} md={10} sm={12}>
              <Title size="lg">Τίτλοι</Title>
            </Grid>
            <Grid item md={5} sm={12} xs={12} style={{ marginBottom: "2vh" }}>
              <SearchBar
                onChange={handleSearch}
                value={searchForm.search}
                placeholder="Αναζητήστε εδώ..."
                style={{ maxWidth: 450 }}
                onCancelSearch={handleSearch}
              />
            </Grid>
          </PageTitle>
          <Grid item xs={12}>
            <Grid container direction="row" justify="center">
             <Grid item xl={7} lg={7} md={7} sm={12} xs={12}>
                <Grid item xs={12} style={{ textAlign: "right" }}>
                  <NormalText>
                    <CallToActionButton href="/titles">Πιστοποήσεις</CallToActionButton>
                  </NormalText>
                </Grid>
                <Grid item xs={6} style={{ textAlign: "left" }}>
                  <NormalText>
                    <b>{rest.total}</b> διαθέσιμα δεδομένα
                  </NormalText>
                </Grid>
                <Grid item xs={12} style={{ textAlign: "center", marginTop: "10px" }}>
                  <Title size="md">Κοινοποιήσεις Τίτλων</Title>
                </Grid>
                <List>
                  {titles &&
                    titles.map((row, index) => (
                      <div key={index}>
                        <SharedTitleItem {...row} />
                        {index + 1 <= titles.length && <Divider />}
                      </div>
                    ))}
                </List>
                <Pagination
                  className={styles.page}
                  count={getPageTotal()}
                  color="primary"
                  size="large"
                  page={searchForm.offset}
                  onChange={handlePageChange}
                />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Main>
    </VerifierLayout>
  );
}
