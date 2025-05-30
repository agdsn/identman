
import {hashCache} from "./helpers";

export interface Data {
    nhash: number;
    query: string;
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
const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function getAdditionalContent(query: string, n: number) {
    const result = await hashCache(query, n);
    const response = await fetch("http://127.0.0.1:5000/api/challenge", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
        body: JSON.stringify(result),
    }
);
    return {
        "query": query,
        "salt": result.salt,
    }
}

