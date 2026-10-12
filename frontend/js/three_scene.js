// ============================================================
// VISION - 3D Particle Humanoid HUD
// ============================================================
let scene, camera, renderer, particleSystem, particleGeometry;
let basePositions = [];
let currentScale = 1.0, targetScale = 1.0;
let targetRotationY = 0, currentRotationY = 0;

const PARTICLE_COUNT = 8000;

function init() {
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x050508, 0.02);

    camera = new THREE.PerspectiveCamera(60,
        window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 12;

    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    document.getElementById("canvas-container").appendChild(renderer.domElement);

    createParticleHumanoid();
    window.addEventListener("resize", onWindowResize);

    // Hook into WS events
    VisionWS.onMessage((data) => {
        if (data.type !== "hand_data") return;
        HUDController.update(data);
        targetScale = data.scale ?? targetScale;
        if (data.rotation) targetRotationY += data.rotation * 0.5;
        if (data.trigger) {
            targetScale = 1.5;
            updateVoiceStatus("HUD ACTIVATED");
            VoiceVisualizer.flash();
        }
    });

    animate();
}

function createParticleHumanoid() {
    particleGeometry = new THREE.BufferGeometry();
    const positions = new Float32Array(PARTICLE_COUNT * 3);
    const colors    = new Float32Array(PARTICLE_COUNT * 3);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        const idx = i * 3;
        let x, y, z;
        const r = Math.random();

        if (r < 0.3) {              // Head
            const theta = Math.random() * Math.PI * 2;
            const phi   = Math.acos(2 * Math.random() - 1);
            const rad   = 0.8 + Math.random() * 0.2;
            x = rad * Math.sin(phi) * Math.cos(theta);
            y = 2.5 + rad * Math.cos(phi);
            z = rad * Math.sin(phi) * Math.sin(theta);
        } else if (r < 0.7) {       // Torso
            x = (Math.random() - 0.5) * 1.2;
            y = 0.5 + Math.random() * 1.5;
            z = (Math.random() - 0.5) * 0.6;
        } else {                    // Limbs
            const limb  = Math.floor(Math.random() * 4);
            const angle = Math.random() * Math.PI * 2;
            const rad   = Math.random() * 0.3;
            x = (limb < 2 ? 0.8 : -0.8) + rad * Math.cos(angle);
            y = (limb % 2 === 0 ? 0.2 : -1.2) + rad * Math.sin(angle);
            z = rad * Math.cos(angle);
        }

        positions[idx]     = x;
        positions[idx + 1] = y;
        positions[idx + 2] = z;

        const hue = 0.5 + (y * 0.05);
        const c = new THREE.Color().setHSL(hue % 1, 1.0, 0.6);
        colors[idx]     = c.r;
        colors[idx + 1] = c.g;
        colors[idx + 2] = c.b;
    }

    particleGeometry.setAttribute("position",
        new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute("color",
        new THREE.BufferAttribute(colors, 3));
    basePositions = positions.slice();

    const material = new THREE.PointsMaterial({
        size: 0.05, vertexColors: true, transparent: true,
        opacity: 0.8, blending: THREE.AdditiveBlending,
        depthWrite: false, sizeAttenuation: true,
    });

    particleSystem = new THREE.Points(particleGeometry, material);
    scene.add(particleSystem);
}

function animate() {
    requestAnimationFrame(animate);
    currentScale     += (targetScale     - currentScale)     * 0.08;
    currentRotationY += (targetRotationY - currentRotationY) * 0.05;

    if (particleSystem) {
        particleSystem.scale.setScalar(currentScale);
        particleSystem.rotation.y = currentRotationY;
        particleSystem.rotation.x = Math.sin(Date.now() * 0.0005) * 0.05;
    }
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

window.addEventListener("DOMContentLoaded", init);