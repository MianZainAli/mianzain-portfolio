document.addEventListener('DOMContentLoaded', () => {
    // Add nav scroll handling
    const nav = document.querySelector('.nav');
    const scrollThreshold = 50;

    function handleScroll() {
        if (window.scrollY > scrollThreshold) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }

    window.addEventListener('scroll', handleScroll);
    
    const container = document.querySelector('.emoji-background');
    const heroSection = document.querySelector('.hero');
    const emojis = [
        '⚡️', '💻', '🚀', '✨', '💡', '🎯', '🌟', '🔥', '⭐️', '🎨',
        '❤️', '💖', '💝', '💕', '💫', '🌈', '🎮', '🎵', '🎧', '🌸',
        '✅', '💪', '🏆', '🎉', '🎸', '🎹', '🎼', '🎪', '🎭', '🦾',
        '🎯', '🎲', '🎳', '🎨', '🎭', '🎪', '🎢', '🎡', '🎠', '🌈',
        '🌟', '✨', '💫', '⭐️', '🌙', '☀️', '🌍', '🎵', '🎶', '🎺'
    ];
    
    if (!container || !heroSection) {
        console.error('Required elements not found!');
        return;
    }

    function createEmoji() {
        const emoji = document.createElement('span');
        emoji.className = 'floating-emoji';
        emoji.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        
        // Random position from left
        emoji.style.left = Math.random() * 100 + '%';
        
        // Random size variation
        const size = 35 + Math.random() * 15; // Random size between 35px and 50px
        emoji.style.fontSize = `${size}px`;
        
        // Random rotation
        const rotation = Math.random() * 200;
        emoji.style.setProperty('--rotation', `${rotation}deg`);
        
        container.appendChild(emoji);
        
        // Remove emoji after animation or when scrolled past hero section
        setTimeout(() => {
            emoji.remove();
        }, 16000); // Match this with animation duration
    }

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Start emoji creation
                const emojiInterval = setInterval(createEmoji, 2000);
                // Store interval ID on the section element
                heroSection.dataset.emojiInterval = emojiInterval;
            } else {
                // Clear interval when section is not visible
                clearInterval(Number(heroSection.dataset.emojiInterval));
                // Clear existing emojis
                container.innerHTML = '';
            }
        });
    }, { threshold: 0.1 });

    observer.observe(heroSection);

    // Initial emojis
    for(let i = 0; i < 6; i++) {
        setTimeout(createEmoji, Math.random() * 2000);
    }

    // Add smooth scroll handling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return; // Skip if it's just '#'
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const navHeight = document.querySelector('.nav').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = targetPosition + window.scrollY - navHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Contact Form Handling
    const contactForm = document.getElementById('contactForm');
    const submitBtn = document.getElementById('submitBtn');
    const buttonText = submitBtn.querySelector('.button-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    function setSubmitting(isSubmitting) {
        const submitBtn = document.getElementById('submitBtn');
        if (isSubmitting) {
            submitBtn.classList.add('loading');
        } else {
            submitBtn.classList.remove('loading');
        }
        submitBtn.disabled = isSubmitting;
    }

    function showError(fieldId, message) {
        const errorSpan = document.getElementById(`${fieldId}Error`);
        if (errorSpan) {
            errorSpan.textContent = message;
            errorSpan.style.display = 'block';
        }
    }

    function clearErrors() {
        ['name', 'email', 'message'].forEach(field => {
            const errorSpan = document.getElementById(`${field}Error`);
            if (errorSpan) {
                errorSpan.textContent = '';
                errorSpan.style.display = 'none';
            }
        });
    }

    function showNotification(message, type = 'default') {
        const notification = document.getElementById('notification');
        const messageElement = notification.querySelector('.notification-message');
        
        // Clear existing classes
        notification.className = 'notification';
        
        // Add new classes
        notification.classList.add('show');
        if (type === 'success' || type === 'error') {
            notification.classList.add(type);
        }
        
        messageElement.textContent = message;
        
        // Hide notification after 5 seconds
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearErrors();
            setSubmitting(true);

            const formData = new FormData(contactForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Accept': 'application/json'
                    },
                    credentials: 'same-origin'
                });

                const data = await response.json();

                if (data.status === 'success') {
                    contactForm.reset();
                    showNotification(data.message, 'success');
                } else {
                    if (data.errors) {
                        Object.entries(data.errors).forEach(([field, messages]) => {
                            showError(field, Array.isArray(messages) ? messages[0] : messages);
                        });
                    } else {
                        showNotification(data.message || 'An error occurred. Please try again.', 'error');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                showNotification('An error occurred. Please try again.', 'error');
            } finally {
                setSubmitting(false);
            }
        });
    }
});

