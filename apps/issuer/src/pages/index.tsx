import React from 'react';
import BasicLayout, {
  Top,
  Content,
  Main,
  Bottom,
} from '@digigov/ui/layouts/Basic';
import Header, {HeaderTitle} from '@digigov/ui/app/Header';
import GovGRLogo from '@digigov/ui/govgr/Logo';
import GovGRFooter from '@digigov/ui/govgr/Footer';
import {makeStyles } from '@material-ui/core';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, {PageTitleHeading} from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import ServiceBadge from '@digigov/ui/core/ServiceBadge';

const useStyles = makeStyles(
  {
    top: {minHeight: '75px'},
    main: {},
    side: {
      
    },
  },
  {name: 'MuiSite'}
);

export default function Index() {
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
      <Content>
        <Main className={styles.main}>
          <PageTitle>
            <PageTitleHeading>Service name</PageTitleHeading>
          </PageTitle>
          <Paragraph>Welcome text</Paragraph>
          <CallToActionButton href="/login?next=/diplomas">Enter here</CallToActionButton>
        </Main>
      </Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
}
