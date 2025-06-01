import React, {useEffect, useState} from 'react';
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
    console.log(query);
    const loadAdditionalContent = async (data: Data) => {
        setLoading(prev => ({ ...prev, additionalContent: true }));
        try {
            console.log(data)


            const content = await getAdditionalContent(data.query, data.nHash, data.csrfToken);
            console.log(content)
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

                <div className="additional-content">

                    {loading.additionalContent ? (
                        renderLoadingSpinner()
                    ) : errors.contentError ? (
                        <div className="error">{errors.contentError}</div>
                    ) : (
                        additionalContent && (
                            <pre>
                                {additionalContent.error ? (
                                    <pre>
                                        <h2 className="error">Validierung Fehlgschlagen!</h2>
                                        <div>{additionalContent.error}</div>
                                    </pre>
                                ) : (
                                    <pre>
                                        <h2 className="validated">Aktives Mitglied der AG DSN:</h2>
                                        <div className="daten">
                                            <div>Name: {additionalContent.fname} {additionalContent.name}</div>
                                            <div>Geburtsjahr: {additionalContent.byear}</div>
                                            <div>ist nur gültig mit einen Lichtbildausweis!</div>
                                        </div>
                                    </pre>
                                )}
                            </pre>
                        )
                    )}
                </div>
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
