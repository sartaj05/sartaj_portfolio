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
    }
    if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: .12 });
    document.querySelectorAll('[data-reveal]').forEach((element, index) => {
        element.style.transitionDelay = `${Math.min(index * 45, 240)}ms`;
        revealObserver.observe(element);
    });

    const skillObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll('[data-width]').forEach(meter => meter.style.width = meter.dataset.width);
                skillObserver.unobserve(entry.target);
            }
        });
    }, { threshold: .3 });
    document.querySelectorAll('.skill-group').forEach(group => skillObserver.observe(group));

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
