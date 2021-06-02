import React from 'react';
import { Main } from '@digigov/ui/layouts/Basic';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, { PageTitleHeading } from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import Layout from "@diplomas/design-system/Layout";

export default function Index() {
  return (
    
    <Layout>
      <Main >
        <PageTitle>
          <PageTitleHeading>Titles holder service</PageTitleHeading>
        </PageTitle>
        <Paragraph>You can issue diploma in the blockchain</Paragraph>
        <CallToActionButton href="/login?next=/titles">Enter here</CallToActionButton>
      </Main>
    </Layout>
  )
    
}
