import React from 'react';
import { Main } from '@digigov/ui/layouts/Basic';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, { PageTitleHeading } from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import VerifierLayout from 'verifier/components/VerifierLayout';

export default function Index() {
  return (
    <VerifierLayout>
      <Main >
        <PageTitle>
          <PageTitleHeading>Verifier service</PageTitleHeading>
        </PageTitle>
        <Paragraph>You can issue diploma in the blockchain</Paragraph>
        <CallToActionButton href="/login?next=/shares">Start here</CallToActionButton>
      </Main>
    </VerifierLayout>
  )
    
}
