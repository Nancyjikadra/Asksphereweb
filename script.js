document.addEventListener('DOMContentLoaded', () => {
    const parallaxLayers = document.querySelectorAll('.parallax-layer');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY;
        
        parallaxLayers.forEach((layer, index) => {
            const speed = (index + 1) * 0.5;
            const yPos = -(scrolled * speed);
            layer.style.transform = `translateY(${yPos}px)`;
        });
    });
});

// Interaction functionality

let currentFeedback = null;

function handleLove() {
    updateFeedback('loved');
}

function handleLike() {
    updateFeedback('liked');
}

function handleDisappointed() {
    updateFeedback('disappointed');
}

function updateFeedback(newFeedback) {
    const lovedBtn = document.querySelector('.loved-btn');
    const likedBtn = document.querySelector('.liked-btn');
    const disappointedBtn = document.querySelector('.disappointed-btn');

    // Reset all buttons
    lovedBtn.classList.remove('active');
    likedBtn.classList.remove('active');
    disappointedBtn.classList.remove('active');

    // If clicking the same button, deactivate it
    if (currentFeedback === newFeedback) {
        currentFeedback = null;
        return;
    }

    // Set new feedback
    currentFeedback = newFeedback;
    
    // Activate the clicked button
    switch(newFeedback) {
        case 'loved':
            lovedBtn.classList.add('active');
            break;
        case 'liked':
            likedBtn.classList.add('active');
            break;
        case 'disappointed':
            disappointedBtn.classList.add('active');
            break;
    }
}

let usefulnessState = null;

function markUseful() {
    const usefulBtn = document.querySelector('.useful-btn');
    const notUsefulBtn = document.querySelector('.not-useful-btn');

    if (usefulnessState === 'useful') {
        usefulBtn.classList.remove('active');
        usefulnessState = null;
    } else {
        usefulBtn.classList.add('active');
        notUsefulBtn.classList.remove('active');
        usefulnessState = 'useful';
    }
}

function markNotUseful() {
    const usefulBtn = document.querySelector('.useful-btn');
    const notUsefulBtn = document.querySelector('.not-useful-btn');

    if (usefulnessState === 'not-useful') {
        notUsefulBtn.classList.remove('active');
        usefulnessState = null;
    } else {
        notUsefulBtn.classList.add('active');
        usefulBtn.classList.remove('active');
        usefulnessState = 'not-useful';
    }
}
