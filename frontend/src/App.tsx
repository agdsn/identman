import React, {useEffect, useRef, useState} from 'react';
import {useSearchParams} from 'react-router-dom';
import logo from './agdsn_logo_weiß.png';
import './App.css';
import './index.css';
import {getHello, getAdditionalContent, Data, Validated} from './api';

interface LoadingState {
    initialData: boolean;
    additionalContent: boolean;
}

interface ErrorState {
    initialError: string | null;
    contentError: string | null;
}



function App() {
    //const location = useLocation();
    //const searchParams = new URLSearchParams(location.search);
    const hasFetched = useRef(false);
    console.log("calling App")
      const [searchParams, setSearchParams] = useSearchParams();



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
                contentError: error instanceof Error ? error.message : 'Ein Fehler ist aufgetreten'
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
                    throw Error("Invalider QR Code");
                }
                const data: Data = await getHello(query);
                setInitialData(data);
                await loadAdditionalContent(data);
            } catch (error) {
                setErrors(prev => ({
                    ...prev,
                    initialError: error instanceof Error ? error.message : 'Ein Fehler ist aufgetreten'
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
            <p>Laden...</p>
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

            <div className="content-container">
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
                                        <h2 className="error">Validierung Fehlgschlagen!</h2>
                                        <div>{additionalContent.error}</div>
                                    </pre>
                                    </div>
                                ) : (
                                    <>
                                        <div className="additional-content">
                                                <pre>
                                                    <h2 className="validated">Aktives Mitglied der AG DSN:</h2>
                                                    <div className="daten">
                                                        <div>Name: {additionalContent.fname} {additionalContent.name}</div>
                                                        <div>{additionalContent.byear && (
                                                            <span>Geburtsjahr: {additionalContent.byear}</span>
                                                        )}</div>

                                                    </div>
                                                </pre>
                                        </div>
                                        <div className="grey">ist nur gültig mit einen Lichtbildausweis!</div>
                                    </>
                                )}
                            </pre>


                )
                )}
            </div>
        );
    };
  return (
    <div className="App background-container">
    <div className="blur-overlay">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />



              {renderContent()}

      </header>
    </div>
      </div>
  );
}

export default App;
