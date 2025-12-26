import React, {useEffect, useRef, useState} from 'react';
import {useSearchParams} from 'react-router-dom';
import logo from './agdsn_logo_weiß.png';
import './App.css';
import './index.css';
import { useTranslation } from 'react-i18next';
import i18n from './translation';

export default function Profil() {
    const { t, i18n: i18nInstance } = useTranslation();




  return (
    <div>
      <h2>{t("AG DSN ident")}</h2>

        <p>{t('We are maintaining and ensuring the development of the network in the dormitories of the Studentenwerk Dresden.')}</p>
        <p>{t('This application serve the identification of active participating in the AG DSN.')}</p>
        <p>{t('Thorougher information\'s can be found on')} <a href="https://www.studentenwerk-dresden.de/wohnen/internet.html">{t('Studentenwerk Dresden')}</a></p>
    </div>
  );
}