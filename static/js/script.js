document.addEventListener('DOMContentLoaded', () => {
    const counters = document.querySelectorAll('.counter');
    
    counters.forEach(counter => {
        counter.innerText = '0';
        
        const updateCounter = () => {
            const target = +counter.getAttribute('data-target');
            const c = +counter.innerText;
            
            // Speed control factor
            const increment = target / 100;
            
            if(c < target) {
                counter.innerText = `${Math.ceil(c + increment)}`;
                setTimeout(updateCounter, 20);
            } else {
                counter.innerText = target + "+";
            }
        };
        
        // Basic element view observer triggers
        const observer = new IntersectionObserver((entries) => {
            if(entries[0].isIntersecting) {
                updateCounter();
                observer.disconnect();
            }
        }, { threshold: 0.5 });
        
        observer.observe(counter);
    });
});
// 4. HERO BACKGROUND AUTOMATIC LOOPING SLIDER (WITH TEXT VISIBILITY TOGGLE)
    const slides = document.querySelectorAll('.hero-slide');
    const heroContent = document.querySelector('.hero-content-wrapper');
    
    if (slides.length > 0 && heroContent) {
        let currentSlideIndex = 0;

        setInterval(() => {
            // Remove active class from current image
            slides[currentSlideIndex].classList.remove('active');
            
            // Calculate next slide index row
            currentSlideIndex = (currentSlideIndex + 1) % slides.length;
            
            // Add active class to next image
            slides[currentSlideIndex].classList.add('active');

            // 👇 THIRD IMAGE (Index 2) வரும்போது மட்டும் டெக்ஸ்டை மறைக்கிறோம்
            if (currentSlideIndex === 3) {
                heroContent.classList.add('text-hidden');
            } else {
                heroContent.classList.remove('text-hidden');
            }
        }, 5000); // Transitions automatically every 5 seconds
    }
const modal = document.getElementById('productModal');
    const viewButtons = document.querySelectorAll('.view-details-btn');
    const closeTrigger = document.querySelector('.close-modal-trigger');

    if(modal && viewButtons.length > 0) {
        viewButtons.forEach(button => {
            button.addEventListener('click', () => {
                document.getElementById('modalProductTitle').innerText = button.getAttribute('data-title');
                document.getElementById('modalProductImg').setAttribute('src', button.getAttribute('data-img'));
                document.getElementById('modalProductDesc').innerText = button.getAttribute('data-desc');
                modal.style.display = 'flex';
            });
        });
        closeTrigger.addEventListener('click', () => { modal.style.display = 'none'; });
        window.addEventListener('click', (e) => { if (e.target === modal) { modal.style.display = 'none'; } });
    }
    // 5. MOBILE HAMBURGER MENU INTERACTIVE SIDE DRAWER
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinksMenu = document.getElementById('navLinksMenu');

    if (mobileMenuBtn && navLinksMenu) {
        mobileMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevents instant auto-closing window triggers
            
            // Toggle side drawer active class
            navLinksMenu.classList.toggle('mobile-nav-active');
            
            // Icon-ஐ 'Bars' லிருந்து 'X' (Close) குறியீடாக மாற்றுகிறோம்
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinksMenu.classList.contains('mobile-nav-active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark');
            } else {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        });

        // மெனுவுக்கு வெளியே எங்கு கிளிக் செய்தாலும் சைடு மெனு தானாகவே மூடிக்கொள்ளும்
        document.addEventListener('click', (e) => {
            if (!navLinksMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                navLinksMenu.classList.remove('mobile-nav-active');
                const icon = mobileMenuBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }
        });
    }