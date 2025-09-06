// Interactive features for the bookstore

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Book card hover effects
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 20px rgba(0,0,0,0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
        });
    });

    // Search functionality enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // Add a small delay before searching (debounce)
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                // You could add AJAX search here
                console.log('Searching for:', this.value);
            }, 500);
        });
    }

    // Add to cart functionality (demo)
    const addToCartButtons = document.querySelectorAll('.btn-primary');
    addToCartButtons.forEach(button => {
        if (button.textContent.includes('Add to Cart')) {
            button.addEventListener('click', function() {
                // Simulate adding to cart
                this.textContent = 'Added!';
                this.style.background = '#27ae60';
                setTimeout(() => {
                    this.textContent = 'Add to Cart';
                    this.style.background = '#3498db';
                }, 2000);
            });
        }
    });

    // Mobile menu toggle (if needed)
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Loading animation for images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        img.addEventListener('error', function() {
            this.style.background = '#f0f0f0';
            this.style.color = '#666';
            this.innerHTML = 'Image not found';
        });
    });

    // Dynamic content loading indicator
    function showLoadingIndicator() {
        const loader = document.createElement('div');
        loader.className = 'loading-indicator';
        loader.innerHTML = 'Loading...';
        loader.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 20px;
            border-radius: 5px;
            z-index: 1000;
        `;
        document.body.appendChild(loader);
        
        setTimeout(() => {
            if (loader.parentNode) {
                loader.parentNode.removeChild(loader);
            }
        }, 2000);
    }

    // Add click events for demonstration
    const demoLinks = document.querySelectorAll('a[href="#"]');
    demoLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            showLoadingIndicator();
        });
    });
});