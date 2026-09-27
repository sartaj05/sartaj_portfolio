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
    const scrollBehavior = () => document.documentElement.dataset.motion === 'full' ? 'smooth' : 'auto';
    if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: scrollBehavior() }));

    document.querySelectorAll('a[href^="#"]').forEach(anchor => anchor.addEventListener('click', event => {
        const target = document.getElementById(anchor.hash.slice(1));
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: scrollBehavior(), block: 'start' });
        if (anchor.classList.contains('skip-link')) {
            target.setAttribute('tabindex', '-1');
            target.focus({ preventScroll: true });
        }
    }));

    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('[data-project-tags]');
    const emptyFilter = document.querySelector('.empty-filter');
    filterButtons.forEach(button => button.addEventListener('click', () => {
        // Capture positions before the grid changes so the motion layer can animate reflow.
        document.dispatchEvent(new CustomEvent('portfolio:filter-start'));
        filterButtons.forEach(item => item.classList.remove('active'));
        filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        button.classList.add('active');
        const filter = button.dataset.filter;
        let visible = 0;
        projectCards.forEach(card => {
            const tags = card.dataset.projectTags || '';
            const show = filter === 'all' || (filter === 'data'
                ? /data|openai|ai\/ml|chatbot|streamlit/.test(tags)
                : tags.includes(filter));
            card.style.display = show ? '' : 'none';
            if (show) visible += 1;
        });
        if (emptyFilter) emptyFilter.hidden = visible !== 0;
        document.dispatchEvent(new CustomEvent('portfolio:filter-end'));
    }));
    filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item.classList.contains('active'))));

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
