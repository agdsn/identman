import {hashCache} from "./helpers";

export interface Data {
    nHash: number;
    query: string;
    csrfToken: string;
    signedToken: string;
}

export interface Validated {
    error?: string;
    fname?: string;
    name?: string;
    byear?: number;
}

const api = import.meta.env.VITE_API || "http://127.0.0.1:8000";

export async function getHello(query: string): Promise<Data> {
  console.log("api: " + api)
  const response = await fetch(`${api}/api?query=` + query, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
      credentials: "include"
        }
    );
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

  return response.json();
}

export async function getAdditionalContent(query: string, n: number, csrfToken: string): Promise<Validated> {
    const result = await hashCache(query, n, csrfToken);
    const response = await fetch(`${api}/api/challenge`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
            credentials: "include",
            body: JSON.stringify(result),
        }
    );
    return response.json();
}

