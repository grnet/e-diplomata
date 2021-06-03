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

export default function Documents({ children, ...props }) {
    const router = useRouter();
    const [documents, setDocuments] = useState([]);
    const [searchForm, setSearchForm] = useState({
        limit: 10,
        offset: 1,
    });

    const styles = useStyles();
    const { data, fetch, ...rest } = useResourceMany("issuer/documents", searchForm);
    
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
            if (options === props.types) {
                const deleteKeySearchForm = delete searchForm.type;
                setSearchForm((searchForm) => ({
                    ...searchForm,
                    ...deleteKeySearchForm,
                    offset: 1,
                }));
            }
            if (options === props.departments) {
                const deleteKeySearchForm = delete searchForm.department;
                setSearchForm((searchForm) => ({
                    ...searchForm,
                    ...deleteKeySearchForm,
                    offset: 1,
                }));
            }
        } else {
            if (options === props.types) {
                setSearchForm((searchForm) => ({
                    ...searchForm,
                    type: value,
                    offset: 1,
                }));
            }
            if (options === props.departments) {
                setSearchForm((searchForm) => ({
                    ...searchForm,
                    department: value,
                    offset: 1,
                }));
            }
        }
    }

    useEffect(() => {
        setDocuments(data);
    }, [data]);

    useEffect(() => {
        fetch();
    }, [searchForm]);

   /*  const createDeploma = function () {
        router.push("/diplomas/create");
    }; */

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
                                types={props.types}
                                departments={props.departments}
                                handleChange={handleChange}
                            />
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
                                    {documents &&
                                        documents.map((row, index) => (
                                            <div key={index}>
                                                {React.Children.map(children, child => (
                                                    React.cloneElement(child, { ...row })
                                                ))}
                                                {index + 1 <= documents.length && <Divider />}
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
        </Layout>
    );
}
