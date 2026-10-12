// Simple voice activity visualizer (visual only, backend drives text)
const VoiceVisualizer = (() => {
    let indicator = null;

    function init() {
        indicator = document.querySelector(".voice-indicator");
    }

    function flash(color = "#00ffcc") {
        if (!indicator) return;
        indicator.style.background = color;
        indicator.style.boxShadow = `0 0 20px ${color}`;
        setTimeout(() => {
            indicator.style.background = "#00ffcc";
            indicator.style.boxShadow = "0 0 10px #00ffcc";
        }, 400);
    }

    return { init, flash };
})();

window.addEventListener("DOMContentLoaded", VoiceVisualizer.init);