const SSL_ENABLED = window.config.SSL_ENABLED == "True";
const BASE_API_URL = window.config.BASE_API_URL;
const HTTP_PREFIX = SSL_ENABLED ? 'https' : 'http';
const WS_PREFIX = SSL_ENABLED ? 'wss' : 'ws';
const HTTP_BASE_URL = `${HTTP_PREFIX}://${BASE_API_URL}/api`
const WS_BASE_URL = `${WS_PREFIX}://${BASE_API_URL}/api`

export async function generate(API_KEY, resource, params, onEnd) {
    const headers = {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
    };
    var start;

    try {
        start = Date.now();
        const response = await fetch(`${HTTP_BASE_URL}/${resource}/generate`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(params)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log(`Received ${resource} in ${(Date.now() - start) / 1000}s:`);
        console.log(data);
        if (onEnd) {
            onEnd(data);
        }

        return data;
    } catch (error) {
        console.error(`Error occurred while fetching ${resource}: `, error);
    }

    return [];
}

export function stream(API_KEY, resource, params, onMessage) {
    const message = { type: "request", api_key: API_KEY, data: params }
    const ws = new WebSocket(`${WS_BASE_URL}/${resource}/stream`);
    var start;

    ws.onopen = function () {
        start = Date.now();
        console.log(`WebSocket opened for ${resource}`)
        ws.send(JSON.stringify(message));
    }

    ws.onmessage = function incoming(event) {
        const data = JSON.parse(event.data);
        if (data.type == "item") {
            console.log(data.data);
            onMessage(data.data);
        } else if (data.type == "end") {
            ws.close();
        }
    };

    ws.onerror = function (error) {
        console.error(`Error on WebSocket for ${resource}`, error)
    };

    ws.onclose = function (event) {
        console.log(`WebSocket closed for ${resource} after ${(Date.now() - start) / 1000}s`)
    }
}
