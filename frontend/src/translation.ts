import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import translationEN from './locales/en.json';
import translationDE from './locales/de.json';

i18n
  .use(LanguageDetector) // Optional: Automatische Spracherkennung
  .use(initReactI18next) // Binden an React
  .init({
    resources: {
      en: {
        translation: translationEN,
      },
      de: {
        translation: translationDE,
      },
    },
    lng: 'en', // Standardsprache
    fallbackLng: 'en', // Falls eine Übersetzung fehlt
    interpolation: {
      escapeValue: false, // XSS-Schutz: In der Regel auf 'true' setzen, aber für Testzwecke oft deaktiviert
    },
  });

export default i18n;