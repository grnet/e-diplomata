import React from 'react';
import BasicLayout, { Bottom, Top, Content } from "@digigov/ui/layouts/Basic";
import GovGRFooter from "@digigov/ui/govgr/Footer";
import GovGRLogo from "@digigov/ui/govgr/Logo";
import Header, { HeaderTitle } from "@digigov/ui/app/Header";
import { makeStyles } from "@material-ui/core";
import ServiceBadge from "@digigov/ui/core/ServiceBadge";

const useStyles = makeStyles(
    {
        top: { minHeight: "75px" },
    },
    { name: "MuiSite" }
);

export default function HolderLayout({ children }) {
    const styles = useStyles();
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
            <Content>{children}</Content>
            <Bottom>
                <GovGRFooter />
            </Bottom>
        </BasicLayout>
    );
}