import PropTypes from 'prop-types';
import React from 'react';
import { useTranslation } from 'react-i18next';
import dynamic from 'next/dynamic';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { AuthProvider, useToken } from '@digigov/auth';
import initI18n from '@digigov/nextjs/i18n';
import NextLink from '@digigov/nextjs/Link';
import { APIProvider, APIErrors } from '@digigov/ui/api';
import I18NProvider from '@digigov/ui/app/i18n';
import { LinkProvider } from '@digigov/ui/core/Link';
import GovGRTheme from '@digigov/ui/themes/govgr';
import el from '../locales/el';

initI18n({
  el: {
    translation: el,
  },
});

const DigiGOVApp = dynamic(() => import('@digigov/ui/app/App'), { ssr: false });

const CONFIG = {
  baseURL: '/api',
};
const AUTH_CONFIG = {};
AUTH_CONFIG.userDataURL = CONFIG.baseURL + '/issuer/me/';
AUTH_CONFIG.loginURL = CONFIG.baseURL + '/issuer/login/';
AUTH_CONFIG.tokenURL = CONFIG.baseURL + '/token/';


export const HandleError = ({ error }) => {
  if (error.name === 'APIError') {
    error = error.error;
    if (error.status === 401) {
      window.location.replace('/login');
      return <div>Unauthorized</div>;
    }
  }
  return <div>Unknown error</div>;
};

HandleError.propTypes = {
  error: PropTypes.shape({
    error: PropTypes.any,
    name: PropTypes.string,
    status: PropTypes.number,
  }),
};

const APIWrapper = ({ children }) => {
  const token = useToken();
  return (
    <APIErrors fallback={HandleError}>
      <APIProvider token={token} config={CONFIG}>
        {children}
      </APIProvider>
    </APIErrors>
  );
};

APIWrapper.propTypes = {
  children: PropTypes.any,
};

export const DigiGOVNextApp = ({ Component, pageProps, theme }) => {
  const router = useRouter();
  const { t, i18n } = useTranslation();
  return (
    <LinkProvider component={NextLink}>
      <Head>
        <meta
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width"
        />
      </Head>
      <DigiGOVApp theme={theme}>
        <I18NProvider t={t} i18n={i18n}>
          <AuthProvider
            config={AUTH_CONFIG}
            navigate={(url) => {
              console.debug('Auth navigation to ', url);
              router.push(url);
            }}
          >
            <APIWrapper>
              <Component {...pageProps} />
            </APIWrapper>
          </AuthProvider>
        </I18NProvider>
      </DigiGOVApp>
    </LinkProvider>
  );
};


DigiGOVNextApp.propTypes = {
  Component: PropTypes.any,
  pageProps: PropTypes.any,
  theme: PropTypes.any,
};

DigiGOVNextApp.defaultProps = {
  theme: GovGRTheme,
};

export default DigiGOVNextApp;
