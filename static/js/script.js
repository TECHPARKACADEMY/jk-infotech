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