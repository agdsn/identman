
interface HashResult {
    hash: string;
    salt: string;
}

export interface HashcashResult {
     query: string;
     n: number;
     salt: string;
     csrfToken: string;
}

function getZerosString(n: number): string {
  return '0'.repeat(n);
}

async function hashWithSalt(value: string, nonce: string): Promise<HashResult> {
    const encoder = new TextEncoder();
    const data = encoder.encode(value);
    const nonce_data = encoder.encode(nonce);
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    const combined = new Uint8Array(data.length + array.length + nonce_data.length);
    combined.set(data);
    combined.set(nonce_data,  data.length);
    combined.set(array, data.length + nonce_data.length);

    const hashBuffer = await window.crypto.subtle.digest('SHA-512', combined);
    const hash = Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
    const salt = Array.from(new Uint8Array(array))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

    return { hash, salt };
}

export async function hashCache(query: string, n: number, csrfToken: string): Promise<HashcashResult> {
    const leading_zeros = getZerosString(n);

    while (true) {
        const result = await hashWithSalt(query, csrfToken);

        if (result.hash.startsWith(leading_zeros)){
            console.log(query + " " + csrfToken)
            return {
                query: query,
                n: n,
                salt: result.salt,
                csrfToken: csrfToken
            };
        }
    }
}

