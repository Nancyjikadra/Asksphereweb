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
let likeCount = 0;
let dislikeCount = 0;
let usefulnessState = null;

function handleLike() {
    const likeBtn = document.querySelector('.like-btn');
    const dislikeBtn = document.querySelector('.dislike-btn');
    const likeCountSpan = document.querySelector('.like-count');

    if (likeBtn.classList.contains('active')) {
        likeBtn.classList.remove('active');
        likeCount--;
    } else {
        likeBtn.classList.add('active');
        likeCount++;
        if (dislikeBtn.classList.contains('active')) {
            dislikeBtn.classList.remove('active');
            dislikeCount--;
            document.querySelector('.dislike-count').textContent = dislikeCount;
        }
    }
    likeCountSpan.textContent = likeCount;
}

function handleDislike() {
    const likeBtn = document.querySelector('.like-btn');
    const dislikeBtn = document.querySelector('.dislike-btn');
    const dislikeCountSpan = document.querySelector('.dislike-count');

    if (dislikeBtn.classList.contains('active')) {
        dislikeBtn.classList.remove('active');
        dislikeCount--;
    } else {
        dislikeBtn.classList.add('active');
        dislikeCount++;
        if (likeBtn.classList.contains('active')) {
            likeBtn.classList.remove('active');
            likeCount--;
            document.querySelector('.like-count').textContent = likeCount;
        }
    }
    dislikeCountSpan.textContent = dislikeCount;
}

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
