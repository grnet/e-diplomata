import initI18n from '@digigov/nextjs/i18n';

import App from '@digigov/nextjs/App';
initI18n({
  el: {
    translation: require('../locales/el'),
  },
});
export default App;
