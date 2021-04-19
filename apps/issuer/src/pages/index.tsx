import React from 'react';
import  { Main } from '@digigov/ui/layouts/Basic';
import Paragraph from '@digigov/ui/typography/Paragraph';
import PageTitle, {PageTitleHeading} from '@digigov/ui/app/PageTitle';
import CallToActionButton from '@digigov/ui/core/Button/CallToAction';
import GenericTemplate from 'src/components/genericTemplate';

/* const useStyles = makeStyles(
  {
    main: {},
    side: {
      
    },
  },
  {name: 'MuiSite'}
); */

export default function Index() {
  /* const styles = useStyles(); */
  return (
    <GenericTemplate>
      <Main >
          <PageTitle>
            <PageTitleHeading>Service name</PageTitleHeading>
          </PageTitle>
          <Paragraph>Welcome text</Paragraph>
          <CallToActionButton href="/login?next=/diplomas">Enter here</CallToActionButton>
        </Main>
    </GenericTemplate>
  );
}
