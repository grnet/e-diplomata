import React from 'react';
import  { Main } from '@digigov/ui/layouts/Basic';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, {PageTitleHeading} from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import IssuerLayout from 'src/components/IssuerLayout';


export default function Index() {
  return (
    <IssuerLayout>
      <Main >
          <PageTitle>
            <PageTitleHeading>Ediplomas issuer service</PageTitleHeading>
          </PageTitle>
          <Paragraph>You can issue diploma in the blockchain</Paragraph>
          <CallToActionButton href="/login?next=/diplomas">Enter here</CallToActionButton>
        </Main>
    </IssuerLayout>
  );
}
