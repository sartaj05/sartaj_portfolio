/* Portfolio choreography. Native browser animations; no runtime dependency. */
(() => {
    'use strict';

    const root = document.documentElement;
    const systemMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
    let userPaused = false;
    try { userPaused = localStorage.getItem('portfolio-motion') === 'paused'; } catch (_) { /* Storage may be blocked. */ }
    const allowed = () => !systemMotion.matches && !userPaused;
    root.dataset.motion = allowed() ? 'full' : 'reduced';

    document.addEventListener('DOMContentLoaded', () => {
        const toggle = document.getElementById('motionToggle');
        const activeAnimations = new Set();
        const seen = new WeakSet();
        const headings = new WeakMap();
        const revealElements = [...document.querySelectorAll('[data-reveal]')];
        const pointerTargets = [...document.querySelectorAll('.tilt-card, .magnetic')];
        const stage = document.querySelector('.hero-stage');
        const timelines = [...document.querySelectorAll('.lab-timeline')];
        const cards = [...document.querySelectorAll('[data-project-tags]')];
        const motionSurfaces = [...document.querySelectorAll('.hero-stage, .page-index-card, .project-card, .signal-strip, .lab-timeline, .lab-experience, .profile-card, .contact-terminal-card')];
        const ease = 'cubic-bezier(.16, 1, .3, 1)';
        let scrollFrame = 0;
        let pointerFrame = 0;
        let pointer = null;
        let hovered = null;
        let beforeFilter = new Map();
        let revealObserver;

        // All content is visible without JS. Animations temporarily replace that resting state.
        const animate = (element, frames, options = {}) => {
            if (!element || !allowed() || document.hidden || typeof element.animate !== 'function') return;
            const animation = element.animate(frames, { duration: 800, easing: ease, fill: 'both', ...options });
            activeAnimations.add(animation);
            animation.addEventListener('finish', () => {
                activeAnimations.delete(animation);
                animation.cancel(); // Release compositing layers and leave the normal CSS state.
            }, { once: true });
            animation.addEventListener('cancel', () => activeAnimations.delete(animation), { once: true });
            return animation;
        };

        const enter = (element, delay = 0, distance = '0 24px') => animate(element, [
            { opacity: 0, translate: distance },
            { opacity: 1, translate: '0 0' }
        ], { delay });

        // Keep the original heading for assistive technology; the visual copy is decorative.
        document.querySelectorAll('h1, .section-heading-lab h2, .cta-lab h2').forEach(heading => {
            const visual = document.createElement('span');
            visual.className = 'motion-heading-visual';
            visual.setAttribute('aria-hidden', 'true');
            [...heading.childNodes].forEach(node => visual.appendChild(node.cloneNode(true)));
            const walker = document.createTreeWalker(visual, NodeFilter.SHOW_TEXT);
            const textNodes = [];
            while (walker.nextNode()) textNodes.push(walker.currentNode);
            const words = [];
            textNodes.forEach(node => {
                const fragment = document.createDocumentFragment();
                node.textContent.split(/(\s+)/).forEach(part => {
                    if (!part.trim()) { fragment.appendChild(document.createTextNode(part)); return; }
                    const mask = document.createElement('span');
                    const word = document.createElement('span');
                    mask.className = 'motion-word-mask';
                    word.className = 'motion-word';
                    word.textContent = part;
                    mask.appendChild(word);
                    fragment.appendChild(mask);
                    words.push(word);
                });
                node.replaceWith(fragment);
            });
            const readable = document.createElement('span');
            readable.className = 'motion-sr-only';
            while (heading.firstChild) readable.appendChild(heading.firstChild);
            heading.append(readable, visual);
            headings.set(heading, words);
        });

        const reveal = (element) => {
            if (seen.has(element)) return;
            seen.add(element);
            element.classList.add('is-visible');
            const title = element.querySelector('h1, .section-heading-lab h2, .cta-lab h2');
            if (title && headings.has(title)) {
                headings.get(title).forEach((word, index) => animate(word, [
                    { translate: '0 115%', rotate: '4deg', opacity: 0 },
                    { translate: '0 0', rotate: '0deg', opacity: 1 }
                ], { duration: 950, delay: Math.min(index * 65, 520) }));
                const children = element.classList.contains('hero-copy') ? element.children : element.querySelectorAll('p, .section-number, .text-link, .btn');
                [...children].filter(child => child !== title).forEach((child, i) => enter(child, 90 + Math.min(i * 85, 400)));
            } else {
                const siblings = [...element.parentElement.children].filter(child => child.hasAttribute('data-reveal'));
                const delay = Math.min(Math.max(0, siblings.indexOf(element)) * 80, 240);
                enter(element, delay, element.classList.contains('timeline-item') ? '28px 0' : '0 28px');
            }
            if (element.classList.contains('hero-stage')) {
                element.querySelectorAll('.terminal-content > *, .stack-node').forEach((line, i) => enter(line, 280 + i * 90, '0 12px'));
                element.querySelectorAll('.orbit-label').forEach((label, i) => enter(label, 850 + i * 100));
            }
            element.querySelectorAll('[data-width]').forEach((meter, index) => {
                meter.style.width = meter.dataset.width;
                animate(meter, [{ scale: '0 1' }, { scale: '1 1' }], { duration: 1100, delay: index * 65 });
            });
        };

        if ('IntersectionObserver' in window) {
            revealObserver = new IntersectionObserver(entries => {
                entries.forEach(entry => {
                    if (!entry.isIntersecting) return;
                    reveal(entry.target);
                    revealObserver.unobserve(entry.target);
                });
            }, { threshold: 0, rootMargin: '0px 0px -24px 0px' });
            revealElements.forEach(element => revealObserver.observe(element));
            const surfaceObserver = new IntersectionObserver(entries => {
                entries.forEach(entry => entry.target.classList.toggle('motion-in-view', entry.isIntersecting));
            }, { rootMargin: '80px' });
            motionSurfaces.forEach(element => surfaceObserver.observe(element));
        } else {
            revealElements.forEach(element => {
                element.classList.add('is-visible');
                element.querySelectorAll('[data-width]').forEach(meter => { meter.style.width = meter.dataset.width; });
            });
            motionSurfaces.forEach(element => element.classList.add('motion-in-view'));
        }

        // Duplicate only the decorative marquee track, with a second copy hidden from AT.
        const track = document.querySelector('.signal-track');
        const group = track?.querySelector('.signal-group');
        if (group) {
            const clone = group.cloneNode(true);
            clone.setAttribute('aria-hidden', 'true');
            clone.classList.add('signal-group-copy');
            track.appendChild(clone);
        }

        const paintScroll = () => {
            scrollFrame = 0;
            if (document.hidden) return;
            if (stage) {
                const rect = stage.getBoundingClientRect();
                const travel = Math.max(-1, Math.min(1, (window.innerHeight / 2 - rect.top - rect.height / 2) / window.innerHeight));
                stage.style.setProperty('--stage-shift', allowed() && finePointer.matches ? `${travel * 30}px` : '0px');
            }
            timelines.forEach(timeline => {
                const rect = timeline.getBoundingClientRect();
                const progress = allowed() ? Math.max(0, Math.min(1, (window.innerHeight * .72 - rect.top) / rect.height)) : 1;
                timeline.style.setProperty('--timeline-progress', progress);
            });
        };
        const scheduleScroll = () => {
            if (!scrollFrame && !document.hidden) scrollFrame = requestAnimationFrame(paintScroll);
        };
        window.addEventListener('scroll', scheduleScroll, { passive: true });
        window.addEventListener('resize', scheduleScroll, { passive: true });
        scheduleScroll();

        const resetPointer = () => {
            if (pointerFrame) cancelAnimationFrame(pointerFrame);
            pointerFrame = 0;
            pointer = null;
            pointerTargets.forEach(element => {
                element.style.removeProperty('transform');
                element.classList.remove('motion-hover');
            });
            hovered = null;
        };
        const paintPointer = () => {
            pointerFrame = 0;
            if (!pointer || !allowed() || !finePointer.matches || document.hidden) return;
            root.style.setProperty('--pointer-x', `${pointer.x}px`);
            root.style.setProperty('--pointer-y', `${pointer.y}px`);
            if (!hovered) return;
            const { element, rect } = hovered;
            const x = Math.max(-.5, Math.min(.5, (pointer.x - rect.left) / rect.width - .5));
            const y = Math.max(-.5, Math.min(.5, (pointer.y - rect.top) / rect.height - .5));
            element.style.setProperty('--shine-x', `${(x + .5) * 100}%`);
            element.style.setProperty('--shine-y', `${(y + .5) * 100}%`);
            element.style.transform = element.classList.contains('magnetic')
                ? `translate(${x * 10}px, ${y * 8}px)`
                : `perspective(1100px) rotateX(${y * -7}deg) rotateY(${x * 9}deg) translateY(-4px)`;
        };
        window.addEventListener('pointermove', event => {
            if (!allowed() || !finePointer.matches || event.pointerType === 'touch') return;
            pointer = { x: event.clientX, y: event.clientY };
            if (!pointerFrame) pointerFrame = requestAnimationFrame(paintPointer);
        }, { passive: true });
        pointerTargets.forEach(element => {
            element.addEventListener('pointerenter', event => {
                if (!allowed() || !finePointer.matches || event.pointerType === 'touch' || element.disabled) return;
                hovered = { element, rect: element.getBoundingClientRect() };
                element.classList.add('motion-hover');
            });
            const leave = () => {
                element.style.removeProperty('transform');
                element.classList.remove('motion-hover');
                if (hovered?.element === element) hovered = null;
            };
            element.addEventListener('pointerleave', leave);
            element.addEventListener('pointercancel', leave);
        });
        window.addEventListener('scroll', resetPointer, { passive: true });
        window.addEventListener('blur', resetPointer);
        finePointer.addEventListener('change', resetPointer);

        // FLIP: preserve the old positions, then animate the new grid arrangement.
        document.addEventListener('portfolio:filter-start', () => {
            activeAnimations.forEach(animation => animation.cancel());
            resetPointer();
            beforeFilter = new Map(cards.filter(card => card.style.display !== 'none').map(card => [card, card.getBoundingClientRect()]));
        });
        document.addEventListener('portfolio:filter-end', () => {
            cards.filter(card => card.style.display !== 'none').forEach((card, i) => {
                card.classList.add('is-visible');
                seen.add(card);
                revealObserver?.unobserve(card);
                const previous = beforeFilter.get(card);
                if (previous) {
                    const rect = card.getBoundingClientRect();
                    animate(card, [{ translate: `${previous.left - rect.left}px ${previous.top - rect.top}px` }, { translate: '0 0' }], { duration: 550 });
                } else {
                    enter(card, Math.min(i * 40, 160), '0 18px');
                }
            });
            scheduleScroll();
        });

        const syncMotion = () => {
            root.dataset.motion = allowed() ? 'full' : 'reduced';
            resetPointer();
            if (!allowed()) {
                activeAnimations.forEach(animation => animation.cancel());
                revealElements.forEach(element => {
                    element.classList.add('is-visible');
                    element.querySelectorAll('[data-width]').forEach(meter => { meter.style.width = meter.dataset.width; });
                });
            }
            if (toggle) {
                toggle.hidden = false;
                toggle.disabled = systemMotion.matches;
                toggle.setAttribute('aria-pressed', String(!allowed()));
                toggle.setAttribute('aria-label', systemMotion.matches
                    ? 'Animations paused by device preference'
                    : (allowed() ? 'Pause animations' : 'Resume animations'));
                toggle.querySelector('[data-motion-label]').textContent = allowed() ? 'Motion on' : 'Motion paused';
                toggle.title = systemMotion.matches ? 'Animations follow your device’s reduced motion setting' : 'Pause or resume decorative animations';
            }
            scheduleScroll();
        };
        toggle?.addEventListener('click', () => {
            userPaused = !userPaused;
            try { localStorage.setItem('portfolio-motion', userPaused ? 'paused' : 'full'); } catch (_) { /* Preference still applies this visit. */ }
            syncMotion();
        });
        systemMotion.addEventListener('change', syncMotion);
        document.addEventListener('visibilitychange', () => {
            root.classList.toggle('motion-background', document.hidden);
            if (document.hidden) {
                resetPointer();
                if (scrollFrame) cancelAnimationFrame(scrollFrame);
                scrollFrame = 0;
                activeAnimations.forEach(animation => animation.cancel());
            } else { scheduleScroll(); }
        });
        syncMotion();
    });
})();
