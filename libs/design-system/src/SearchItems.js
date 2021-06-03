import React from "react";

import PageTitle from "@digigov/ui/app/PageTitle";
import { Title } from "@digigov/ui/typography";
import Grid from "@material-ui/core/Grid";
import SearchBar from "@diplomas/design-system/SearchBar";

export default function SearchItems({ handleSearch, ...props }) {
    return (
        <>
            <PageTitle>
                <Grid item xs={12} md={10} sm={12}>
                    <Title size="lg">Διπλώματα</Title>
                </Grid>
                <Grid item xs={5} style={{ marginBottom: "2vh" }}>
                    <SearchBar
                        onChange={handleSearch}
                        value={props.search}
                        placeholder="Αναζητήστε εδώ..."
                        style={{ maxWidth: 450 }}
                        onCancelSearch={handleSearch}
                    />
                </Grid>
            </PageTitle>
        </>
    );
}
