// Frontend gesture state machine (visual feedback hooks)
const GestureState = (() => {
    let current = "idle";
    const handlers = {};

    function on(gesture, fn) { handlers[gesture] = fn; }

    function set(gesture) {
        if (gesture === current) return;
        current = gesture;
        if (handlers[gesture]) handlers[gesture]();
    }

    function get() { return current; }

    return { on, set, get };
})();