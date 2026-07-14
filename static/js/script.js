document.addEventListener('DOMContentLoaded', () => {
    
    // 1. HERO SLIDESHOW ROTATION INTERFACE
// 1. HERO SLIDESHOW ROTATION INTERFACE (WITH INTEGRATED LAST SLIDE CONTENT AUTO-HIDER)
    const heroSlides = document.querySelectorAll('.hero-slide');
    const heroContentData = document.getElementById('heroContentData');

    if (heroSlides.length > 0 && heroContentData) {
        let currentSlideIndex = 0;
        
        setInterval(() => {
            // Removes active layout nodes from old index tracking frames
            heroSlides[currentSlideIndex].classList.remove('active');
            
            // Increments forward into next circular iteration node
            currentSlideIndex = (currentSlideIndex + 1) % heroSlides.length;
            
            // Appends standard activation overlay target rules
            heroSlides[currentSlideIndex].classList.add('active');

            // VALIDATION FACTOR: Checks if current viewport target matches 4th image (Index 3)
            if (currentSlideIndex === 3) {
                // Instantly triggers opacity down values inside style sheets
                heroContentData.classList.add('content-hidden-state');
            } else {
                // Restores layout typography layers automatically for slides 1, 2 and 3
                heroContentData.classList.remove('content-hidden-state');
            }
        }, 5000); // Rotates configuration matrices sequentially every 5 seconds
    }

    // 2. PRODUCT CARDS REDIRECTION TO WHATSAPP DESK (DIRECT CONNECTIVITY FROM PORTFOLIO)
    const productCards = document.querySelectorAll('.product-clickable-card');
    productCards.forEach(card => {
        card.addEventListener('click', () => {
            const productName = card.getAttribute('data-product') || 'Hardware Systems';
            const whatsappNumber = "918056828383";
            const customMsg = `Hello JK InfoTech, I Am Interested In Buying / Enquiring About "${productName}". Please Share The Details and Pricing Models.`;
            
            // Constructs a secure custom URL API path string 
            const encryptedUrl = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(customMsg)}`;
            window.open(encryptedUrl, '_blank');
        });
    });

    // 3. ANIMATED COUNTER CONTROLLERS
    const statsCounters = document.querySelectorAll('.counter');
    if (statsCounters.length > 0) {
        const triggerCountersAnimation = (counterElement) => {
            const numericalTarget = +counterElement.getAttribute('data-target');
            let initialCount = 0;
            const operationalSpeed = numericalTarget / 60; // Smooth increment progression layout
            
            const refreshValue = () => {
                if (initialCount < numericalTarget) {
                    initialCount += operationalSpeed;
                    counterElement.innerText = Math.ceil(initialCount) + "+";
                    setTimeout(refreshValue, 25);
                } else {
                    counterElement.innerText = numericalTarget + "+";
                }
            };
            refreshValue();
        };

        // Standard Scroll Observer Intersection configuration
        const scrollObserver = new IntersectionObserver((observedEntries) => {
            observedEntries.forEach(entry => {
                if (entry.isIntersecting) {
                    triggerCountersAnimation(entry.target);
                    scrollObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.7 });

        statsCounters.forEach(counter => scrollObserver.observe(counter));
    }

    // 4. MOBILE DRAWER INTERACTION HUB
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinksMenu = document.getElementById('navLinksMenu');

    if (mobileMenuBtn && navLinksMenu) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            navLinksMenu.classList.toggle('mobile-nav-active');
            const toggleIcon = mobileMenuBtn.querySelector('i');
            if (navLinksMenu.classList.contains('mobile-nav-active')) {
                toggleIcon.classList.replace('fa-bars', 'fa-xmark');
            } else {
                toggleIcon.classList.replace('fa-xmark', 'fa-bars');
            }
        });

        document.addEventListener('click', (e) => {
            if (!navLinksMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navLinksMenu.classList.remove('mobile-nav-active');
                const toggleIcon = mobileMenuBtn.querySelector('i');
                if (toggleIcon) toggleIcon.classList.replace('fa-xmark', 'fa-bars');
            }
        });
    }
});
// ==========================================================================
// DYNAMIC PRODUCT MINI WINDOW MODAL HANDLING ENGINE
// ==========================================================================
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("productMiniWindow");
    const closeBtn = document.querySelector(".close-window-btn");
    const viewButtons = document.querySelectorAll(".view-details-btn");

    // Modal DOM fields inside wrapper
    const modalImg = document.getElementById("modalProductImg");
    const modalName = document.getElementById("modalProductName");
    const modalDesc = document.getElementById("modalProductDesc");
    const modalWaLink = document.getElementById("modalWhatsAppRedirect");

    if (viewButtons.length > 0 && modal) {
        viewButtons.forEach(button => {
            button.addEventListener("click", function (e) {
                e.preventDefault();
                
                // Extracting variables using data tags attributes safely
                const name = this.getAttribute("data-name");
                const desc = this.getAttribute("data-desc");
                const img = this.getAttribute("data-image");
                const whatsappUrl = this.getAttribute("data-whatsapp");

                // Inject dynamic parameters safely into modal framework
                modalName.textContent = name;
                modalDesc.textContent = desc || "Premium corporate configuration build layout ready.";
                modalImg.src = img;
                modalWaLink.href = whatsappUrl;

                // Fire overlay block visible state mechanics
                modal.style.display = "flex";
            });
        });

        // Close functions triggers logic
        closeBtn.addEventListener("click", () => modal.style.display = "none");
        
        window.addEventListener("click", function (e) {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });
    }
});