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
/* import Pagination from "@material-ui/lab/Pagination"; */
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import SearchBar from "issuer/components/searchBar";
import { debounce } from "lodash";
import DiplomaItem from "src/components/diplomaItem";
import GenericTemplate from "src/components/genericTemplate";

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
  /* const [dataset, setDataset] = useState(); */
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

  function handleChange({ value }, options, removeBoxItem) {
    if (removeBoxItem) {
      if (options === datasets.degree) {
        const deleteKeySearchForm = delete searchForm.degree;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
        }));
      }
      if (options === datasets.typeOfDegree) {
        const deleteKeySearchForm = delete searchForm.typeOfDegree;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
        }));
      }
      if (options === datasets.school) {
        const deleteKeySearchForm = delete searchForm.school;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
        }));
      }
      if (options === datasets.institution) {
        const deleteKeySearchForm = delete searchForm.institution;
        setSearchForm((searchForm) => ({
          ...searchForm,
          ...deleteKeySearchForm,
        }));
      }
    } else {
      if (options === datasets.degree) {
        setSearchForm((searchForm) => ({ ...searchForm, degree: value }));
      }
      if (options === datasets.typeOfDegree) {
        setSearchForm((searchForm) => ({ ...searchForm, typeOfDegree: value }));
      }
      if (options === datasets.school) {
        setSearchForm((searchForm) => ({ ...searchForm, school: value }));
      }
      if (options === datasets.institution) {
        setSearchForm((searchForm) => ({ ...searchForm, institution: value }));
      }
    }
  }

  useEffect(() => {
    setDiplomas(data);
  }, [data]);

  /* useEffect(() => {
    setSearchForm(searchForm);
  }, [searchForm]); */

  useEffect(() => {
    fetch();
  }, [searchForm]);

  const createDeploma = function () {
    router.push("/diplomas/create");
  };

  return (
    <GenericTemplate>
      <Main xs={12} md={12} className={styles.main}>
        <Grid container direction="column">
          <PageTitle>
            <Grid item xs={12} md={10} sm={12}>
              <Title size="lg">Διπλώματα</Title>
            </Grid>
            <Grid item md={6} sm={12} xs={12} style={{ marginBottom: "2vh" }}>
              <SearchBar
                onChange={handleInput}
                value={searchForm.search}
                placeholder="Αναζητήστε εδώ..."
                style={{ maxWidth: 450 }}
              />
            </Grid>
          </PageTitle>
          <Grid item xs={12}>
            <Grid container direction="row">
              <Grid item xl={4} lg={4} md={4} sm={8} xs={12}>
                <Title size="md">Φίλτρα αναζήτησης</Title>
                <Grid item>
                  <NormalText variant="body1">Τίτλος σπουδών</NormalText>
                </Grid>
                <Grid item xs={12}>
                  {datasets && (
                    <ComboBox
                      value={searchForm.degree}
                      options={datasets.degree}
                      onChange={handleChange}
                      variant="standard"
                    ></ComboBox>
                  )}
                </Grid>
                <Grid item>
                  <NormalText variant="body1">Είδος τίτλου σπουδών</NormalText>
                </Grid>
                <Grid item xs={12}>
                  {datasets && (
                    <ComboBox
                      value={searchForm.typeOfDegree}
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
                      value={searchForm.school}
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
                      value={searchForm.institution}
                      options={datasets.institution}
                      onChange={handleChange}
                      variant="standard"
                    ></ComboBox>
                  )}
                </Grid>
              </Grid>
              <Grid item xl={7} lg={7} md={7}>
                <Grid container direction={"column"} spacing={2}>
                  <Grid item xs={12} style={{ textAlign: "right" }}>
                    <Button onClick={createDeploma}>
                      Δημιουργία αιτήματος
                    </Button>
                  </Grid>

                  <Grid item xs={12} style={{ textAlign: "center" }}>
                    <Title size="md">Τίτλοι Σπουδών</Title>
                  </Grid>
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
                {/* <Pagination
                        className={styles.page}
                        count={getPageTotal()}
                        color="primary"
                        size="large"
                        page={page.noPage}
                        onChange={handlePageChange}
                      /> */}
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Main>
    </GenericTemplate>
  );
}
