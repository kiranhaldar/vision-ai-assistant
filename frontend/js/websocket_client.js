// WebSocket client with auto-reconnect
const VisionWS = (() => {
    let ws = null;
    let reconnectTimer = null;
    const listeners = [];
    const WS_URL = "ws://localhost:8765";

    function connect() {
        try {
            ws = new WebSocket(WS_URL);
        } catch (e) {
            scheduleReconnect();
            return;
        }

        ws.onopen = () => {
            console.log("[WS] Connected");
            updateVoiceStatus("VISION ONLINE");
        };

        ws.onmessage = (event) => {
            let data;
            try { data = JSON.parse(event.data); }
            catch (e) { console.warn("Bad JSON", e); return; }
            listeners.forEach((fn) => fn(data));
        };

        ws.onclose = () => {
            console.log("[WS] Disconnected");
            updateVoiceStatus("DISCONNECTED");
            scheduleReconnect();
        };

        ws.onerror = (err) => console.error("[WS] Error", err);
    }

    function scheduleReconnect() {
        if (reconnectTimer) return;
        reconnectTimer = setTimeout(() => {
            reconnectTimer = null;
            connect();
        }, 3000);
    }

    function onMessage(fn) { listeners.push(fn); }

    return { connect, onMessage };
})();

function updateVoiceStatus(text) {
    const el = document.getElementById("voice-text");
    if (el) el.textContent = text;
}

// Auto-connect on load
window.addEventListener("DOMContentLoaded", () => VisionWS.connect());