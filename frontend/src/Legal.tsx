import {useTranslation} from "react-i18next";
import React from 'react';

function Legal() {
  const api = import.meta.env.VITE_LEGAL_END || "";
  const { t, i18n: i18nInstance } = useTranslation();
  return (
    <footer>
      <a href={api} className="link footer">{t("Legal Notice")}</a>
      <span> · @2026 AG DSN</span>
    </footer>
  );
}

export default Legal;
