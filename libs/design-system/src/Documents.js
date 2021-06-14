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
import ComboBox from "@diplomas/design-system/ComboBox";
import Grid from "@material-ui/core/Grid";
import { useRouter } from "next/router";
import { useResourceMany } from "@digigov/ui/api";
import { debounce } from "lodash";
import Pagination from "@material-ui/lab/Pagination";
import SearchBar from "@diplomas/design-system/SearchBar";
import Layout from "@diplomas/design-system/Layout";
import ListItems from "@diplomas/design-system/ListItems";
import SearchItems from "@diplomas/design-system/SearchItems";
import FilterItems from "@diplomas/design-system/FilterItems";

const useStyles = makeStyles((theme) => ({
    top: { minHeight: "75px" },
    main: {},
    page: {
        "& > *": {
            marginTop: theme.spacing(2),
        },
    },
}));

export default function Documents({ ...props }) {
    const router = useRouter();
    const [documents, setDocuments] = useState([]);
    const [searchForm, setSearchForm] = useState({
        limit: 10,
        offset: 1,
    });

    const styles = useStyles();
    const { data, fetch, ...rest } = useResourceMany(props.url, searchForm);

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


    function handleChange(value, options, removeBoxItem) {
        if (removeBoxItem) {
            props.dataFilters.forEach(item => {
                if (options === item.filterData) {
                    var typeData = item.filterTypeData;
                    const deleteKeySearchForm = delete searchForm[typeData];
                    setSearchForm((searchForm) => ({
                        ...searchForm,
                        ...deleteKeySearchForm,
                        offset: 1,
                    }));
                }
            });
        } else {

            props.dataFilters.forEach(item => {
                if (options === item.filterData) {
                    var typeData = item.filterTypeData;
                    setSearchForm((searchForm) => ({
                        ...searchForm,
                        [typeData]: value,
                        offset: 1,
                    }));
                }
            });
        }
    }
    useEffect(() => {
        setDocuments(data);
    }, [data]);

    useEffect(() => {
        fetch();
    }, [searchForm]);

    return (
        <Layout>
            <Main xs={12} md={12} className={styles.main}>
                <Grid container direction="column">
                    <SearchItems
                        search={searchForm.search}
                        handleSearch={handleSearch}
                    />
                    <Grid item xs={12}>
                        <Grid container direction="row">
                            <FilterItems
                                dataFilters={props.dataFilters}
                                filterTitles={props.filterTitles}
                                handleChange={handleChange}
                            />
                            <Grid item xl={7} lg={7} md={7} sm={12} xs={12}>
                                <Grid item xs={6} style={{ textAlign: "left" }}>
                                    <NormalText>
                                        <b>{rest.total}</b> διαθέσιμα δεδομένα
                                    </NormalText>
                                </Grid>
                                <Grid item xs={12} style={{ textAlign: "center" }}>
                                    <Title size="md">{props.title}</Title>
                                </Grid>
                                <List>
                                    {documents &&
                                        documents.map((row, index) => {
                                            return (
                                                <div key={index}>
                                                    {props.presentation && <ListItems row={row} presentation={props.presentation} />}
                                                    {index + 1 <= documents.length && <Divider />}
                                                </div>
                                            )

                                        })}
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
        </Layout>
    );
}
