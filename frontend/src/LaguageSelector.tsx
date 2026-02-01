import {useTranslation} from "react-i18next";
import React, {useEffect, useState} from 'react';

function LanguageSelector() {
    const { t, i18n: i18nInstance } = useTranslation();
  const [selectedLanguage, setSelectedLanguage] = useState('');
    const changeLanguage = (lng: string) => {
    i18nInstance.changeLanguage(lng);
    setSelectedLanguage(lng)
  };

  useEffect(() => {
    const browserLanguage = navigator.language.substring(0, 2);

    const initialLanguage: string = browserLanguage != 'de'? "en" : browserLanguage;

    changeLanguage(initialLanguage);
  }, []);

  const handleLanguageChange = (event: { target: { value: any; }; }) => {
    const newLanguage = event.target.value;
    changeLanguage(newLanguage);
  };

  return (
    <header className="Language">
      <select id="language" value={selectedLanguage} onChange={handleLanguageChange}>
        <option value="de">de</option>
        <option value="en">en</option>
      </select>
    </header>
  );
}

export default LanguageSelector;
