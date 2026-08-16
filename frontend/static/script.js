import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.180.0/build/three.module.js";


// --------------------------------
// Scene
// --------------------------------

const scene = new THREE.Scene();


// --------------------------------
// Camera
// --------------------------------

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

camera.position.set(0, 0, 15);


// --------------------------------
// Renderer
// --------------------------------

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

document.body.appendChild(renderer.domElement);


// --------------------------------
// Earth
// --------------------------------

const earthGeometry = new THREE.SphereGeometry(5, 64, 64);

const earthMaterial = new THREE.MeshBasicMaterial({
    color: 0x2266cc,
    wireframe: true
});

const earth = new THREE.Mesh(
    earthGeometry,
    earthMaterial
);

scene.add(earth);
// --------------------------------
// Get real satellite trajectory
// --------------------------------

let satelliteOrbit;

async function loadSatelliteOrbit() {

    try {

        const response = await fetch("/api/satellite");

        const data = await response.json();

        console.log("Satellite data:", data);

        document.getElementById("status").textContent =
            `Satellite: ${data.name}`;

        const points = [];

        data.trajectory.forEach(point => {

            // SGP4 coordinates are in kilometers.
            // Our Earth radius is 5 Three.js units.
            const scale = 5 / 6371;

            const x = point.x * scale;
            const y = point.y * scale;
            const z = point.z * scale;

            points.push(
                new THREE.Vector3(x, y, z)
            );

        });


        // Create the orbital line
        const geometry =
            new THREE.BufferGeometry().setFromPoints(points);

        const material =
            new THREE.LineBasicMaterial({
                color: 0xffff00
            });

        satelliteOrbit =
            new THREE.Line(
                geometry,
                material
            );

        scene.add(satelliteOrbit);

        console.log(
            "Trajectory points:",
            points.length
        );

    } catch (error) {

        console.error(
            "Failed to load satellite:",
            error
        );

        document.getElementById("status").textContent =
            "Failed to load satellite data";

    }
}

loadSatelliteOrbit();


// --------------------------------
// Animation
// --------------------------------

function animate() {

    requestAnimationFrame(animate);

    earth.rotation.y += 0.001;

    renderer.render(
        scene,
        camera
    );
}

animate();


// --------------------------------
// Window resizing
// --------------------------------

window.addEventListener("resize", () => {

    camera.aspect =
        window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

});
