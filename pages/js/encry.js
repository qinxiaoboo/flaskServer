// Convert PEM to Base64
function pemToBase64(pem) {
    return pem.replace(/-----BEGIN PUBLIC KEY-----|-----END PUBLIC KEY-----|\s+/g, '');
}

// Convert Base64 to ArrayBuffer
function base64ToArrayBuffer(base64) {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
}

// Convert PEM to DER
function pemToDer(pem) {
    const base64 = pemToBase64(pem);
    return base64ToArrayBuffer(base64);
}

// Convert ArrayBuffer to Base64
function arrayBufferToBase64(buffer) {
    const uint8Array = new Uint8Array(buffer);
    let binary = '';
    const len = uint8Array.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(uint8Array[i]);
    }
    return window.btoa(binary);
}

// Import PEM key
async function importPublicKey(pem) {
    const der = pemToDer(pem);
    const algorithm = {
        name: 'RSA-OAEP',
        hash: { name: 'SHA-256' }
    };
    return crypto.subtle.importKey(
        'spki',
        der,
        algorithm,
        true,
        ['encrypt']
    );
}

// Encrypt data and encode as Base64
async function encryptData(data) {
    const publicKeyPem = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA57+j81CLTvE8HViRTIss\nU3/sng6pLUb0llNgOppTiSS+eRNfdqZWmPrVabu1Gixx8QFWrhRxQu91eDLYuVAF\nHqQJUIJVB3tAzq33J0DwDp2mXTaSLok5X7FaxBP0akaA4xjf+QhWBrC5CI333taC\nVFLjNZIW2L/y8d4riov/BSvxcDRkBwY1GaCUgi88DNIwj0ynj3fTN6AMNRSnyp8G\nLN4pdyeoF1yTIQ5ZAkVgbTizgrennF/GXG/VW1ukf8rk2JNvExtuxuT+muQj0axS\nbWF0xZtBvl0wCxp4/6HrCcF3UXNILK/heF/aKY7QI+nHNDzk6RL/Tqb5E7T4J5Sd\n8QIDAQAB\n-----END PUBLIC KEY-----\n';

    const key = await importPublicKey(publicKeyPem);
    const encodedData = new TextEncoder().encode(data);

    const encryptedBuffer = await crypto.subtle.encrypt(
        { name: 'RSA-OAEP' },
        key,
        encodedData
    );

    return arrayBufferToBase64(encryptedBuffer);
}
// function encryptData(data){
//     let encrypted=[]
//     _encryptData(data)
//         // .then(response => response.json())
//         .then(encryptedBase64 => {
//             console.log('Encrypted data (Base64):', encryptedBase64);
//         })
//         // .catch(err => console.error('Error:', err));
// }



