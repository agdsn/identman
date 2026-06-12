import React from 'react';
import './index.css';
import { useTranslation } from 'react-i18next';

export default function Profil() {
    const { t, i18n: i18nInstance } = useTranslation();




  return (
    <div>
      <h2>{t("AG DSN ident")}</h2>

        <p>{t('We are responsible for maintaining and developing the network in the dormitories of Studentenwerk Dresden.')}</p>
        <p>{t('This application helps identify active AG DSN members.')}</p>
        <p>{t('Further information is available at')} <a className="link content" href="https://www.studentenwerk-dresden.de/wohnen/internet.html">{t('Studentenwerk Dresden')}</a></p>
    </div>
  );
}