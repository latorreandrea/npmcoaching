document.addEventListener('DOMContentLoaded', () => {
    if (window.AOS) {
        AOS.init({
            once: true,
            duration: 850,
            easing: 'ease-out-cubic',
            offset: 20,
        });
    }

    const navbarEl = document.getElementById('site-navbar');
    const applyNavbarState = () => {
        if (!navbarEl) {
            return;
        }
        navbarEl.classList.toggle('is-scrolled', window.scrollY > 16);
    };

    applyNavbarState();
    window.addEventListener('scroll', applyNavbarState, { passive: true });

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

    const sectionLinks = Array.from(document.querySelectorAll('.premium-nav-link[data-nav-target]'));
    const setActiveLink = (sectionId) => {
        sectionLinks.forEach((link) => {
            const target = link.dataset.navTarget;
            link.classList.toggle('is-active', target === sectionId);
        });
    };

    const observedSections = ['home', 'metodo', 'test', 'testimonials']
        .map((id) => document.getElementById(id))
        .filter(Boolean);

    if (observedSections.length && 'IntersectionObserver' in window) {
        const visibilityMap = new Map();
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    visibilityMap.set(entry.target.id, entry.intersectionRatio);
                } else {
                    visibilityMap.delete(entry.target.id);
                }
            });

            if (!visibilityMap.size) {
                return;
            }

            const [activeSection] = Array.from(visibilityMap.entries()).sort((left, right) => right[1] - left[1])[0];
            setActiveLink(activeSection);
        }, {
            threshold: [0.25, 0.45, 0.65],
            rootMargin: '-18% 0px -46% 0px',
        });

        observedSections.forEach((section) => observer.observe(section));
    }

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
