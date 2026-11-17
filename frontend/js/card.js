const container = document.querySelector(".card-container");
const card = document.querySelector(".card");
const glow = document.querySelector(".glow");
let mouseX = 0;
let mouseY = 0;

let currentRotationX = 0;
let currentRotationY = 0;

let targetRotationX = 0;
let targetRotationY = 0;

let velocityX = 0;
let velocityY = 0;

let previousTime = null;

const stiffness = 300;
const damping = 13.4;

container.addEventListener("mousemove", function (event) {
    mouseX = event.clientX;
    mouseY = event.clientY;

    updateCard();
});

container.addEventListener("mouseleave", function() {
    targetRotationX = 0;
    targetRotationY = 0;
    glow.style.opacity = "0";
});

function updateCard() {
    const rect = container.getBoundingClientRect();
    const localX = mouseX - rect.left;
    const localY = mouseY - rect.top;

    card.style.setProperty("--mouse-x", `${localX}px`);
    card.style.setProperty("--mouse-y", `${localY}px`);

    glow.style.opacity = "1";


    const offsetX = localX - (rect.width/2);
    const offsetY = localY - (rect.height/2);
    targetRotationX = -(offsetY / (rect.height/2)) * 15;
    targetRotationY = offsetX / (rect.width/2) * 15;
}
 
function animate(timestamp) {
    if (previousTime === null) {
        previousTime = timestamp;
    }

    const deltaTime = Math.min((timestamp - previousTime) / 1000, 0.033);
    previousTime = timestamp;

    const forceX = (targetRotationX - currentRotationX) * stiffness;
    const forceY = (targetRotationY - currentRotationY) * stiffness;

    velocityX += forceX * deltaTime;
    velocityY += forceY * deltaTime;

    const dampingFactor = Math.exp(-damping * deltaTime);

    velocityX *= dampingFactor;
    velocityY *= dampingFactor;

    currentRotationX += velocityX * deltaTime;
    currentRotationY += velocityY * deltaTime;

    card.style.transform = `rotateX(${currentRotationX}deg) rotateY(${currentRotationY}deg)`;
    requestAnimationFrame(animate);
}

requestAnimationFrame(animate);