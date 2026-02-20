function navbar() {
    return {
        scrolled: false,
        mobileOpen: false,
        init() {
            const updateState = () => {
                this.scrolled = window.scrollY > 12;
            };

            updateState();
            window.addEventListener('scroll', updateState, { passive: true });
        },
    };
}

window.navbar = navbar;

document.addEventListener('DOMContentLoaded', () => {
    if (window.AOS) {
        AOS.init({
            once: true,
            duration: 850,
            easing: 'ease-out-cubic',
            offset: 20,
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (event) => {
            const targetId = anchor.getAttribute('href');
            if (!targetId || targetId === '#') {
                return;
            }

            const target = document.querySelector(targetId);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        });
    });

    const blobs = document.querySelectorAll('.parallax-blob');
    let ticking = false;

    const applyParallax = () => {
        const offset = window.scrollY * 0.05;

        blobs.forEach((blob, index) => {
            const factor = (index + 1) * 0.35;
            blob.style.transform = `translate3d(0, ${offset * factor}px, 0)`;
        });

        ticking = false;
    };

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(applyParallax);
            ticking = true;
        }
    }, { passive: true });
});
