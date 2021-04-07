import React from 'react';
import Head from 'next/head';
import { useTranslation } from '@digigov/ui/app/i18n';

import BasicLayout, {
  Top,
  Content,
  Main,
  Side,
  Bottom,
} from '@digigov/ui/layouts/Basic';
import Header, { HeaderTitle } from '@digigov/ui/app/Header';
import ServiceBadge from '@digigov/ui/core/ServiceBadge';
import GovGRLogo from '@digigov/ui/govgr/Logo';
import GovGRFooter from '@digigov/ui/govgr/Footer';
import PageTitle, { PageTitleHeading } from '@digigov/ui/app/PageTitle';

const Home: React.FC = () => {
  const { t } = useTranslation();
  return (
    <BasicLayout>
      <Head>
        <title>{t('app.name')}</title>
      </Head>
      <Top>
        <Header>
          <GovGRLogo />
          <HeaderTitle>
            {t('app.name')}
            <ServiceBadge label="ALPHA" />
          </HeaderTitle>
        </Header>
      </Top>
      <Content>
        <Main>
          <PageTitle>
            <PageTitleHeading>{t('app.name')}</PageTitleHeading>
          </PageTitle>
          <div>{t('app.intro_text')}</div>
        </Main>
        <Side></Side>
      </Content>
      <Bottom>
        <GovGRFooter />
      </Bottom>
    </BasicLayout>
  );
};

export default Home;
