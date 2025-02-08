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

