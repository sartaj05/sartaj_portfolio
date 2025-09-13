// Portfolio Animations JavaScript

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeScrollAnimations();
    initializeParticles();
    initializeTypingEffect();
    initializeProgressBars();
    initializeSmoothScrolling();
});

// GSAP Animations (if library is available)
function initializeGSAPAnimations() {
    // Hero section animations
    const heroTimeline = gsap.timeline();
    
    heroTimeline
        .from('.hero-title', {
            duration: 1,
            y: 50,
            opacity: 0,
            ease: 'power2.out'
        })
        .from('.hero-content p', {
            duration: 0.8,
            y: 30,
            opacity: 0,
            ease: 'power2.out'
        }, '-=0.3')
        .from('.hero-buttons', {
            duration: 0.6,
            y: 20,
            opacity: 0,
            ease: 'power2.out'
        }, '-=0.2')
        .from('.hero-image', {
            duration: 1,
            scale: 0.8,
            opacity: 0,
            rotation: 10,
            ease: 'back.out(1.7)'
        }, '-=0.8');

    // Skills section animation
    gsap.fromTo('.skill-category', 
        {
            y: 50,
            opacity: 0,
            scale: 0.9
        },
        {
            y: 0,
            opacity: 1,
            scale: 1,
            duration: 0.8,
            stagger: 0.2,
            ease: 'back.out(1.7)',
            scrollTrigger: {
                trigger: '.skills-section',
                start: 'top 80%',
                end: 'bottom 20%',
                toggleActions: 'play none none reverse'
            }
        }
    );

    // Projects animation
    gsap.fromTo('.project-card',
        {
            scale: 0.8,
            opacity: 0,
            rotateY: 45
        },
        {
            scale: 1,
            opacity: 1,
            rotateY: 0,
            duration: 0.8,
            stagger: 0.15,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: '.featured-projects',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        }
    );

    // Experience timeline animation
    gsap.fromTo('.timeline-item',
        {
            x: 50,
            opacity: 0
        },
        {
            x: 0,
            opacity: 1,
            duration: 0.8,
            stagger: 0.2,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: '.timeline',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        }
    );

    // Contact form animation
    gsap.fromTo('.contact-form',
        {
            scale: 0.9,
            opacity: 0
        },
        {
            scale: 1,
            opacity: 1,
            duration: 0.8,
            ease: 'power2.out',
            scrollTrigger: {
                trigger: '.contact-form',
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            }
        }
    );
}

// Fallback CSS animations
function initializeCSSAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.fade-in-up, .fade-in-scale').forEach(el => {
        observer.observe(el);
    });
}

// Scroll-based animations
function initializeScrollAnimations() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.parallax');
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });

    // Progress bar animations on scroll
    const progressObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target.querySelector('.progress-bar');
                if (progressBar) {
                    const value = progressBar.getAttribute('data-value') || 0;
                    setTimeout(() => {
                        progressBar.style.width = value + '%';
                    }, 200);
                }
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.skill-item').forEach(item => {
        progressObserver.observe(item);
    });
}

// Particle system
function initializeParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;

    const particleCount = 50;
    const particles = [];

    for (let i = 0; i < particleCount; i++) {
        createParticle();
    }

    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        // Random properties
        const size = Math.random() * 4 + 2;
        const opacity = Math.random() * 0.5 + 0.3;
        const duration = Math.random() * 3 + 5;
        const delay = Math.random() * 8;
        
        particle.style.cssText = `
            width: ${size}px;
            height: ${size}px;
            left: ${Math.random() * 100}%;
            opacity: ${opacity};
            animation: particleFloat ${duration}s linear infinite ${delay}s;
        `;
        
        particlesContainer.appendChild(particle);
        particles.push(particle);
    }
}

// Typing effect
function initializeTypingEffect() {
    const typingElements = document.querySelectorAll('.typing-text');
    
    typingElements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        element.style.borderRight = '2px solid #667eea';
        
        let index = 0;
        const typeWriter = () => {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                setTimeout(typeWriter, 100);
            } else {
                // Blinking cursor effect
                setInterval(() => {
                    element.style.borderRight = element.style.borderRight === 'none' 
                        ? '2px solid #667eea' 
                        : 'none';
                }, 500);
            }
        };
        
        // Start typing when element comes into view
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(typeWriter, 500);
                    observer.unobserve(entry.target);
                }
            });
        });
        
        observer.observe(element);
    });
}

// Progress bars animation
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        bar.style.width = '0%';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const value = entry.target.getAttribute('data-value') || 0;
                    setTimeout(() => {
                        entry.target.style.width = value + '%';
                    }, 300);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(bar);
    });
}

// Smooth scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Utility functions
function animateOnScroll(selector, animationClass = 'fade-in-up') {
    const elements = document.querySelectorAll(selector);
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add(animationClass);
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(el => observer.observe(el));
}

// Card hover effects
function initializeCardEffects() {
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (typeof gsap !== 'undefined') {
                gsap.to(card, {
                    y: -10,
                    scale: 1.02,
                    duration: 0.3,
                    ease: 'power2.out'
                });
            } else {
                card.style.transform = 'translateY(-10px) scale(1.02)';
                card.style.transition = 'transform 0.3s ease';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            if (typeof gsap !== 'undefined') {
                gsap.to(card, {
                    y: 0,
                    scale: 1,
                    duration: 0.3,
                    ease: 'power2.out'
                });
            } else {
                card.style.transform = 'translateY(0) scale(1)';
            }
        });
    });
}

// Button ripple effect
function createRippleEffect(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Initialize button effects
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', createRippleEffect);
    });
    
    initializeCardEffects();
});

// CSS for ripple effect
const rippleCSS = `
@keyframes ripple {
    0% {
        transform: scale(0);
        opacity: 1;
    }
    100% {
        transform: scale(2);
        opacity: 0;
    }
}
`;

// Add ripple CSS to document
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// Loading screen animation (if needed)
function initializeLoader() {
    const loader = document.querySelector('.loader');
    if (loader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                loader.style.opacity = '0';
                setTimeout(() => {
                    loader.style.display = 'none';
                }, 500);
            }, 1000);
        });
    }
}

// Initialize loader
initializeLoader();

// Export functions for use in other scripts
window.PortfolioAnimations = {
    animateOnScroll,
    createRippleEffect,
    initializeParticles,
    initializeTypingEffect
};