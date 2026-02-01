import React, {useEffect, useRef, useState} from 'react';
import {useSearchParams} from 'react-router-dom';
import './App.css';
import './index.css';
import {getHello, getAdditionalContent, Data, Validated} from './api';
import Profil from './Help';
import i18n from "./translation";
import {useTranslation} from "react-i18next";

interface LoadingState {
    initialData: boolean;
    additionalContent: boolean;
}

interface ErrorState {
    initialError: string | null;
    contentError: string | null;
}

function App() {
    const { t, i18n: i18nInstance } = useTranslation();
    const hasFetched = useRef(false);
    const [searchParams, _] = useSearchParams();



    const [loading, setLoading] = useState<LoadingState>({
        initialData: true,
        additionalContent: false
    });
    const [errors, setErrors] = useState<ErrorState>({
        initialError: null,
        contentError: null
    });
    const [initialData, setInitialData] = useState<any>(null);
    const [additionalContent, setAdditionalContent] = useState<Validated>();
    const query = searchParams.get("query");
    const loadAdditionalContent = async (data: Data) => {
        setLoading(prev => ({ ...prev, additionalContent: true }));
        try {
            const content = await getAdditionalContent(data.query, data.nHash, data.csrfToken);
            setAdditionalContent(content);
        } catch (error) {
            setErrors(prev => ({
                ...prev,
                contentError: error instanceof Error ? error.message : t("There was an error. Try again later")
            }));
        } finally {
            setLoading(prev => ({ ...prev, additionalContent: false }));
        }
    };

    useEffect(() => {
        if (hasFetched.current) return; // blockt doppelten Call
        hasFetched.current = true;
        const initializeData = async () => {
            try {
                //const query = null;
                if (!query) {
                    throw Error(t("Invalid ID!"));
                }
                const data: Data = await getHello(query);
                setInitialData(data);
                await loadAdditionalContent(data);
            } catch (error) {
                setErrors(prev => ({
                    ...prev,
                    initialError:  t("There was an error in our system, please try again later!")
                }));
            } finally {
                setLoading(prev => ({ ...prev, initialData: false }));
            }
        };

        initializeData();
    }, []);

    const renderLoadingSpinner = () => (
        <div className="loader-container">
            <div className="loader"></div>
            <p>{t("loading...")}</p>
        </div>
    );

    const renderContent = () => {
        if (loading.initialData) {
            return renderLoadingSpinner();
        }

        if (errors.initialError) {
            return <div className="error">{errors.initialError}</div>;
        }

        return (
                <div>
                {loading.additionalContent ? (
                        renderLoadingSpinner()
                    ) : errors.contentError ? (
                        <div className="additional-content">
                            <div className="error">{errors.contentError}</div>
                        </div>
                    ) : (
                        additionalContent && (



                            <pre>
                                {additionalContent.error ? (
                                    <div className="additional-content">
                                    <pre>
                                        <h2 className="error">{t("Validation failed!")}</h2>
                                        <div>{additionalContent.error}</div>
                                    </pre>
                                    </div>
                                ) : (
                                    <>
                                        <div className="additional-content">
                                                <pre>
                                                    <h2 className="validated">{t('Valid AG DSN member ID:')}</h2>
                                                    <div className="daten">
                                                        <div>{t('Owned by:')} {additionalContent.fname} {additionalContent.name}</div>
                                                        <div>{additionalContent.byear && (
                                                            <span>{t('Birth year:')} {additionalContent.byear}</span>
                                                        )}</div>

                                                    </div>
                                                </pre>
                                        </div>
                                        <div className="grey">{t('Valid only with ID.')}</div>
                                    </>
                                )}
                            </pre>
                )
                )}
</div>
        );
    };
  const [currentLanguage, setCurrentLanguage] = useState(i18n.language);
  return (

          <div className="content-container">
                {query? renderContent(): Profil()}
          </div>
  );
}

export default App;
