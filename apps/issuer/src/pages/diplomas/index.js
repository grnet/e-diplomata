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
import ComboBox from "issuer/components/comboBox";
import Grid from "@material-ui/core/Grid";
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import SearchBar from "issuer/components/searchBar";
import { debounce } from "lodash";
import Pagination from "@material-ui/lab/Pagination";
import IssuerLayout from "issuer/components/IssuerLayout";
import DiplomaItem from "issuer/components/diplomaItem";

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

export default function Diplomas() {
  const types = ['Bachelor', 'Master', 'Doctorate']
  const departments = ['Main', 'Science']
  const router = useRouter();
  const [diplomas, setDiplomas] = useState([]);
  const [searchForm, setSearchForm] = useState({
    limit: 10,
    offset: 1,
  });

  const styles = useStyles();
  const { data, fetch, ...rest } = useResourceMany("issuer/documents", searchForm);
  console.log(data);
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

  function handleChange( value, options, removeBoxItem) {
    if (removeBoxItem) {
      if (options === types ) {
        const deleteKeySearchForm = delete searchForm.type;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
          offset: 1,
        }));
      }
      if (options === departments) {
        const deleteKeySearchForm = delete searchForm.department;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
          offset: 1,
        }));
      }
    } else {
      if (options === types) {
        setSearchForm((searchForm) => ({
          ...searchForm,
          type: value,
          offset: 1,
        }));
      }
      if (options === departments) {
        setSearchForm((searchForm) => ({
          ...searchForm,
          department: value,
          offset: 1,
        }));
      }
    }
  }

  useEffect(() => {
    setDiplomas(data);
  }, [data]);

  useEffect(() => {
    fetch();
  }, [searchForm]);

  const createDeploma = function () {
    router.push("/diplomas/create");
  };

  return (
    <IssuerLayout>
      <Main xs={12} md={12} className={styles.main}>
        <Grid container direction="column">
          <PageTitle>
            <Grid item xs={12} md={10} sm={12}>
              <Title size="lg">Διπλώματα</Title>
            </Grid>
            <Grid item xs={5} style={{ marginBottom: "2vh" }}>
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
                  {types && <ComboBox
                    options={types}
                    onChange={handleChange}
                    variant="standard"
                  ></ComboBox>}
                </Grid>
                <Grid item>
                  <NormalText variant="body1">Ίδρυμα</NormalText>
                </Grid>
                <Grid item xs={12}>
                  <ComboBox
                    options={departments}
                    onChange={handleChange}
                    variant="standard"
                  ></ComboBox>
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
                  {diplomas &&
                    diplomas.map((row, index) => (
                      <div key={index}>
                        <DiplomaItem {...row} />
                        {index + 1 <= diplomas.length && <Divider />}
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
    </IssuerLayout>
  );
}
