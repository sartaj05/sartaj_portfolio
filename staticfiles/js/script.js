document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('siteHeader');
    const progress = document.getElementById('scrollProgress');
    const backToTop = document.getElementById('backToTop');
    const menuToggle = document.querySelector('.menu-toggle');
    const siteNav = document.getElementById('siteNav');

    const updateScrollUI = () => {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        const percent = max > 0 ? (window.scrollY / max) * 100 : 0;
        if (progress) progress.style.width = `${percent}%`;
        if (header) header.classList.toggle('scrolled', window.scrollY > 24);
        if (backToTop) backToTop.classList.toggle('visible', window.scrollY > 450);
    };
    window.addEventListener('scroll', updateScrollUI, { passive: true });
    updateScrollUI();

    if (menuToggle && siteNav) {
        menuToggle.addEventListener('click', () => {
            const open = siteNav.classList.toggle('open');
            menuToggle.setAttribute('aria-expanded', open);
        });
        siteNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => siteNav.classList.remove('open')));
        window.addEventListener('resize', () => {
            if (window.innerWidth > 680) {
                siteNav.classList.remove('open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        }, { passive: true });
    }
    if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reducedMotion) {
        // A quiet cursor spotlight gives the page a sense of depth without adding noise.
        window.addEventListener('pointermove', event => {
            document.documentElement.style.setProperty('--pointer-x', `${event.clientX}px`);
            document.documentElement.style.setProperty('--pointer-y', `${event.clientY}px`);
        }, { passive: true });

        // Physical-feeling hover depth for the terminal and capability/project cards.
        document.querySelectorAll('.tilt-card').forEach(card => {
            card.addEventListener('pointermove', event => {
                const rect = card.getBoundingClientRect();
                const x = (event.clientX - rect.left) / rect.width - .5;
                const y = (event.clientY - rect.top) / rect.height - .5;
                card.style.transform = `perspective(900px) rotateX(${y * -4}deg) rotateY(${x * 5}deg) translateY(-4px)`;
            });
            card.addEventListener('pointerleave', () => { card.style.transform = ''; });
        });

        // Small magnetic pull on primary actions.
        document.querySelectorAll('.magnetic').forEach(button => {
            button.addEventListener('pointermove', event => {
                const rect = button.getBoundingClientRect();
                const x = event.clientX - rect.left - rect.width / 2;
                const y = event.clientY - rect.top - rect.height / 2;
                button.style.transform = `translate(${x * .08}px, ${y * .12}px)`;
            });
            button.addEventListener('pointerleave', () => { button.style.transform = ''; });
        });
    }

    document.querySelectorAll('a[href^="#"]').forEach(anchor => anchor.addEventListener('click', event => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
    }));

    const revealElements = document.querySelectorAll('[data-reveal]');
    revealElements.forEach((element, index) => {
        element.style.transitionDelay = `${Math.min(index * 45, 240)}ms`;
    });
    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: .12 });
        revealElements.forEach(element => revealObserver.observe(element));
    } else {
        revealElements.forEach(element => element.classList.add('is-visible'));
    }

    const skillGroups = document.querySelectorAll('.skill-group');
    if ('IntersectionObserver' in window) {
        const skillObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.querySelectorAll('[data-width]').forEach(meter => meter.style.width = meter.dataset.width);
                    skillObserver.unobserve(entry.target);
                }
            });
        }, { threshold: .3 });
        skillGroups.forEach(group => skillObserver.observe(group));
    } else {
        skillGroups.forEach(group => group.querySelectorAll('[data-width]').forEach(meter => meter.style.width = meter.dataset.width));
    }

    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('[data-project-tags]');
    const emptyFilter = document.querySelector('.empty-filter');
    filterButtons.forEach(button => button.addEventListener('click', () => {
        filterButtons.forEach(item => item.classList.remove('active'));
        button.classList.add('active');
        const filter = button.dataset.filter;
        let visible = 0;
        projectCards.forEach(card => {
            const tags = card.dataset.projectTags || '';
            const show = filter === 'all' || tags.includes(filter);
            card.style.display = show ? '' : 'none';
            if (show) visible += 1;
        });
        if (emptyFilter) emptyFilter.hidden = visible !== 0;
    }));

    // Optional Plausible custom event: see which project links attract clicks.
    document.querySelectorAll('.project-links a').forEach(link => link.addEventListener('click', () => {
        if (typeof window.plausible !== 'function') return;
        const project = link.closest('.project-card')?.querySelector('h3')?.textContent?.trim() || 'Unknown project';
        window.plausible('Project link click', { props: { project } });
    }));

    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', async event => {
            event.preventDefault();
            const button = document.getElementById('submitBtn');
            const alertBox = document.getElementById('formAlert');
            const original = button.innerHTML;
            button.disabled = true;
            button.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Sending...';
            try {
                const response = await fetch(form.action, {
                    method: 'POST',
                    body: new FormData(form),
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await response.json();
                if (!response.ok || !data.success) throw new Error(data.message || 'Please try again.');
                alertBox.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
                form.reset();
            } catch (error) {
                alertBox.innerHTML = `<div class="alert alert-warning">${error.message || 'Something went wrong. Please email me directly.'}</div>`;
            } finally {
                button.disabled = false;
                button.innerHTML = original;
            }
        });
    }
});
