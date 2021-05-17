


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
import ComboBox from "holder/components/comboBox";
import Grid from "@material-ui/core/Grid";
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import SearchBar from "holder/components/searchBar";
import { debounce } from "lodash";
import Pagination from "@material-ui/lab/Pagination";
import HolderLayout from "holder/components/HolderLayout";
import TitleItem from "holder/components/TitleItem";

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

export default function Titles() {
  const router = useRouter();
  const [titles, setTitles] = useState([]);
  const [searchForm, setSearchForm] = useState({
    limit: 10,
    offset: 1,
  });

  const styles = useStyles();
  const { data: datasets } = useResource("datasets");
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

  function handleChange({ value }, options, removeBoxItem) {
    if (removeBoxItem) {
      if (options === datasets.typeOfDegree) {
        const deleteKeySearchForm = delete searchForm.typeOfDegree;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
          offset: 1,
        }));
      }
      if (options === datasets.school) {
        const deleteKeySearchForm = delete searchForm.school;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
          offset: 1,
        }));
      }
      if (options === datasets.institution) {
        const deleteKeySearchForm = delete searchForm.institution;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
          offset: 1,
        }));
      }
    } else {
      if (options === datasets.typeOfDegree) {
        setSearchForm((searchForm) => ({
          ...searchForm,
          typeOfDegree: value,
          offset: 1,
        }));
      }
      if (options === datasets.school) {
        setSearchForm((searchForm) => ({
          ...searchForm,
          school: value,
          offset: 1,
        }));
      }
      if (options === datasets.institution) {
        setSearchForm((searchForm) => ({
          ...searchForm,
          institution: value,
          offset: 1,
        }));
      }
    }
  }

  useEffect(() => {
    setTitles(data);
  }, [data]);

  useEffect(() => {
    fetch();
  }, [searchForm]);

  const createDeploma = function () {
    router.push("/titles/create");
  };

  return (
    <HolderLayout>
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
            <Grid container direction="row">
              <Grid item xl={4} lg={4} md={4} sm={12} xs={12}>
                <Grid item>
                  <Title className={styles.title} size="md">
                    Φίλτρα αναζήτησης
                  </Title>
                </Grid>
                <Grid item>
                  <NormalText variant="body1">Είδος τίτλου σπουδών</NormalText>
                </Grid>
                <Grid item xs={12}>
                  {datasets && (
                    <ComboBox
                      options={datasets.typeOfDegree}
                      onChange={handleChange}
                      variant="standard"
                    ></ComboBox>
                  )}
                </Grid>
                <Grid item>
                  <NormalText variant="body1">Σχολή/Τμήμα</NormalText>
                </Grid>
                <Grid item xs={12}>
                  {datasets && (
                    <ComboBox
                      options={datasets.school}
                      onChange={handleChange}
                      variant="standard"
                    ></ComboBox>
                  )}
                </Grid>
                <Grid item>
                  <NormalText variant="body1">Ίδρυμα</NormalText>
                </Grid>
                <Grid item xs={12}>
                  {datasets && (
                    <ComboBox
                      options={datasets.institution}
                      onChange={handleChange}
                      variant="standard"
                    ></ComboBox>
                  )}
                </Grid>
              </Grid>
              <Grid item xl={7} lg={7} md={7} sm={12} xs={12}>
                <Grid item xs={6} style={{ textAlign: "left" }}>
                  <NormalText>
                    <b>{rest.total}</b> διαθέσιμα δεδομένα
                  </NormalText>
                </Grid>
                <Grid item xs={12} style={{ textAlign: "center" }}>
                  <Title size="md">Τίτλοι Σπουδών</Title>
                </Grid>
                <List>
                  {titles &&
                    titles.map((row, index) => (
                      <div key={index}>
                        <TitleItem {...row} />
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
    </HolderLayout>
  );
}
