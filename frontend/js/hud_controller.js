// Updates DOM HUD elements based on incoming data
const HUDController = (() => {
    const els = {};

    function init() {
        els.gesture = document.getElementById("val-gesture");
        els.scale   = document.getElementById("val-scale");
        els.rot     = document.getElementById("val-rot");
        els.rings   = document.querySelectorAll(".hud-ring");
    }

    function update(data) {
        if (!els.gesture) return;
        if (data.gesture) els.gesture.textContent = data.gesture.toUpperCase();
        if (typeof data.scale === "number")
            els.scale.textContent = data.scale.toFixed(2);
        if (typeof data.rotation === "number")
            els.rot.textContent = data.rotation.toFixed(2);

        const s = typeof data.scale === "number" ? data.scale : 1.0;
        els.rings.forEach((r) => {
            r.style.transform = `scale(${1 + (s - 1) * 0.2})`;
        });
    }

    return { init, update };
})();

window.addEventListener("DOMContentLoaded", HUDController.init);