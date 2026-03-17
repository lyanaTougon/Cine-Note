// main.js
document.addEventListener('DOMContentLoaded', () => {
    const featuredImages = document.querySelectorAll('.featured-bg');
    let current = 0;

    const nextBtn = document.querySelector('.featured-controls .next');
    const prevBtn = document.querySelector('.featured-controls .prev');

    if (!nextBtn || !prevBtn || featuredImages.length === 0) return;

    nextBtn.addEventListener('click', () => {
        featuredImages[current].classList.add('slide-left');
        current = (current + 1) % featuredImages.length;
        featuredImages[current].classList.remove('slide-left', 'slide-right');
    });

    prevBtn.addEventListener('click', () => {
        featuredImages[current].classList.add('slide-right');
        current = (current - 1 + featuredImages.length) % featuredImages.length;
        featuredImages[current].classList.remove('slide-left', 'slide-right');
    });
});
