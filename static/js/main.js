document.addEventListener('DOMContentLoaded', () => {
    const COOKIE_CONSENT_KEY = 'cookie_consent_v1';

    const readConsent = () => {
        try {
            const raw = window.localStorage.getItem(COOKIE_CONSENT_KEY);
            if (!raw) {
                return null;
            }
            return JSON.parse(raw);
        } catch (error) {
            return null;
        }
    };

    const emitConsentUpdate = (consent) => {
        window.dispatchEvent(new CustomEvent('cookie:consent-updated', {
            detail: consent,
        }));
    };

    const writeConsent = (consent) => {
        const payload = {
            necessary: true,
            analytics: Boolean(consent.analytics),
            marketing: Boolean(consent.marketing),
            timestamp: new Date().toISOString(),
            version: 1,
        };

        window.localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify(payload));
        emitConsentUpdate(payload);
        return payload;
    };

    const cookieBanner = document.getElementById('cookie-consent');
    const cookieSettingsPanel = document.getElementById('cookie-settings-panel');
    const cookieSettingsToggle = document.querySelector('[data-cookie-action="customize"]');
    const analyticsToggle = document.getElementById('consent-analytics');
    const marketingToggle = document.getElementById('consent-marketing');
    const cookieButtons = document.querySelectorAll('[data-cookie-action]');
    const openCookiePreferences = document.getElementById('open-cookie-preferences');

    const showBanner = () => {
        if (!cookieBanner) {
            return;
        }
        cookieBanner.hidden = false;
        cookieBanner.classList.add('is-visible');
    };

    const hideBanner = () => {
        if (!cookieBanner) {
            return;
        }
        cookieBanner.classList.remove('is-visible');
        cookieBanner.hidden = true;
    };

    const openCookieSettings = () => {
        if (!cookieSettingsPanel || !cookieSettingsToggle) {
            return;
        }
        cookieSettingsPanel.hidden = false;
        cookieSettingsToggle.setAttribute('aria-expanded', 'true');
    };

    const toggleCookieSettings = () => {
        if (!cookieSettingsPanel || !cookieSettingsToggle) {
            return;
        }

        const willOpen = cookieSettingsPanel.hidden;
        cookieSettingsPanel.hidden = !willOpen;
        cookieSettingsToggle.setAttribute('aria-expanded', String(willOpen));
    };

    const applyConsentToToggles = (consent) => {
        if (analyticsToggle) {
            analyticsToggle.checked = Boolean(consent?.analytics);
        }
        if (marketingToggle) {
            marketingToggle.checked = Boolean(consent?.marketing);
        }
    };

    const existingConsent = readConsent();
    if (existingConsent) {
        applyConsentToToggles(existingConsent);
        emitConsentUpdate(existingConsent);
    } else {
        showBanner();
    }

    if (openCookiePreferences) {
        openCookiePreferences.addEventListener('click', (event) => {
            event.preventDefault();
            showBanner();

            const consent = readConsent();
            applyConsentToToggles(consent || { analytics: false, marketing: false });
            openCookieSettings();
        });
    }

    cookieButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const action = button.dataset.cookieAction;

            if (action === 'accept') {
                writeConsent({ analytics: true, marketing: true });
                hideBanner();
                return;
            }

            if (action === 'reject') {
                writeConsent({ analytics: false, marketing: false });
                hideBanner();
                return;
            }

            if (action === 'customize') {
                toggleCookieSettings();
                return;
            }

            if (action === 'save') {
                writeConsent({
                    analytics: analyticsToggle?.checked,
                    marketing: marketingToggle?.checked,
                });
                hideBanner();
            }
        });
    });

    let aosResizeTimer;

    if (window.AOS) {
        AOS.init({
            once: false,
            mirror: true,
            duration: 900,
            easing: 'ease-out-cubic',
            offset: 40,
            anchorPlacement: 'top-bottom',
            throttleDelay: 50,
        });

        window.addEventListener('load', () => {
            AOS.refreshHard();
        });

        window.addEventListener('resize', () => {
            window.clearTimeout(aosResizeTimer);
            aosResizeTimer = window.setTimeout(() => {
                AOS.refresh();
            }, 180);
        });
    }

    const navbarEl = document.getElementById('site-navbar');
    let previousScrollY = window.scrollY;
    let navbarTicking = false;
    const desktopMediaQuery = window.matchMedia('(min-width: 992px)');

    const applyNavbarState = () => {
        if (!navbarEl) {
            return;
        }

        navbarEl.classList.toggle('is-scrolled', window.scrollY > 16);

        if (window.scrollY <= 16) {
            navbarEl.classList.remove('nav-hidden');
            previousScrollY = window.scrollY;
            return;
        }

        if (!desktopMediaQuery.matches) {
            navbarEl.classList.remove('nav-hidden');
            previousScrollY = window.scrollY;
            return;
        }

        if (window.scrollY > previousScrollY + 12) {
            navbarEl.classList.add('nav-hidden');
        } else if (window.scrollY < previousScrollY - 10) {
            navbarEl.classList.remove('nav-hidden');
        }

        previousScrollY = window.scrollY;
    };

    applyNavbarState();
    window.addEventListener('scroll', () => {
        if (!navbarTicking) {
            window.requestAnimationFrame(() => {
                applyNavbarState();
                navbarTicking = false;
            });
            navbarTicking = true;
        }
    }, { passive: true });

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

    const sectionLinks = Array.from(document.querySelectorAll('.nav-link-ux[data-nav-target]'));
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
