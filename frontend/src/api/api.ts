
import {hashCache} from "./helpers";

export interface Data {
    nHash: number;
    query: string;
    csrfToken: string;
}

export interface Validated {
    error?: string;
    fname?: string;
    name?: string;
    byear?: number;
}

export async function getHello(query: string): Promise<Data> {
  const response = await fetch("http://127.0.0.1:5000/api?query=" + query, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        }
    );
  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }


  console.log(response);
  return response.json();
}

export async function getAdditionalContent(query: string, n: number, csrfToken: string): Promise<Validated> {
    const result = await hashCache(query, n, csrfToken);
    console.log(result);
    const response = await fetch("http://127.0.0.1:5000/api/challenge", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
            body: JSON.stringify(result),
        }
    );
    return response.json();
}

