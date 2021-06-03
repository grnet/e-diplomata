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
    const styles = useStyles();
    return (
        <>
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
                    {props.types && <ComboBox
                        options={props.types}
                        onChange={handleChange}
                        variant="standard"
                    ></ComboBox>}
                </Grid>
                <Grid item>
                    <NormalText variant="body1">Ίδρυμα</NormalText>
                </Grid>
                <Grid item xs={12}>
                    {props.departments && <ComboBox
                        options={props.departments}
                        onChange={handleChange}
                        variant="standard"
                    ></ComboBox>}
                </Grid>
            </Grid>
        </>
    );
}
