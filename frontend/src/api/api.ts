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

const api = process.env.REACT_APP_API || "http://127.0.0.1:5000";

export function setCSRFToken(token: string) {
    const expireDate = new Date();
    expireDate.setHours(expireDate.getHours() + 1);

    document.cookie = `csrfToken=${token}; expires=${expireDate.toUTCString()}; path=/; samesite=lax`;
}

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


  console.log(response);
  return response.json();
}

function getCookie(name: string) : string {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith(name + "="))
        ?.split("=");
    console.log(cookieValue);
    // @ts-ignore
    return cookieValue.length > 0 ? cookieValue[1]  : "";
}

export async function getAdditionalContent(query: string, n: number, csrfToken: string): Promise<Validated> {
    const result = await hashCache(query, n, csrfToken);
    console.log(result);
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

