import React, { useEffect, useState, useCallback } from "react";
import { makeStyles } from "@material-ui/core";
import { Title, NormalText } from "@digigov/ui/typography";
import ComboBox from "@diplomas/design-system/ComboBox";
import Grid from "@material-ui/core/Grid";
import Layout from "@diplomas/design-system/Layout"

const useStyles = makeStyles((theme) => ({
    title: {
        marginTop: "-9px",
    },
}));

export default function FilterItems({ handleChange, ...props }) {
    console.log(props.dataFilters);
    const styles = useStyles();
    return (
        <>
            <Grid item xl={4} lg={4} md={4} sm={12} xs={12}>
                <Grid item>
                    <Title className={styles.title} size="md">
                        Φίλτρα αναζήτησης
                    </Title>
                </Grid>
                {props.dataFilters &&
                    props.dataFilters.map((row, index) => (
                        <span key={index}>
                            <Grid item>
                                <NormalText variant="body1">{row.title}</NormalText>
                            </Grid>
                            <Grid item xs={12}>
                                {row.filterData && <ComboBox
                                    options={row.filterData}
                                    onChange={handleChange}
                                    variant="standard"
                                ></ComboBox>}
                            </Grid>
                        </span>
                    ))}
            </Grid>
        </>
    );
}
