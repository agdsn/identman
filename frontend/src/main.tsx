import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter} from "react-router-dom";
import LanguageSelector from './LaguageSelector'

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const langEl = document.getElementById("lang");
if (langEl)
    ReactDOM.createRoot(langEl).render(<LanguageSelector />);

root.render(
  <React.StrictMode>
      <BrowserRouter>
          <App />
      </BrowserRouter>
  </React.StrictMode>
);

reportWebVitals();
