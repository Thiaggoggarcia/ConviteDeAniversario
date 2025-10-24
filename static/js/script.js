document.addEventListener('DOMContentLoaded', () => {
    // ELEMENTOS DO DOM
    const welcomeScreen = document.getElementById('welcome-screen');
    const mainContent = document.getElementById('main-content');
    const guestNameInput = document.getElementById('guest-name-input');
    const enterButton = document.getElementById('enter-button');
    const personalizedGreeting = document.getElementById('personalized-greeting');
    const whatsappIcon = document.getElementById('icon-whatsapp');

    // 1. TELA DE ENTRADA E PERSONALIZAÇÃO
    enterButton.addEventListener('click', () => {
        const guestName = guestNameInput.value.trim();
        if (guestName === "" || !/^[A-Za-zÀ-ÿ\s]+$/.test(guestName)) {
            alert("Por favor, digite seu nome para continuar.");
            return;
        }

        // Armazenar nome no localStorage
        localStorage.setItem('guestName', guestName);
        
        // Exibir saudação personalizada
        personalizedGreeting.textContent = `${guestName}, saiba que cada nova versão é feita de boas histórias — e a sua presença torna essa ainda mais inesquecível 🥂`;
        
        // Transição de telas
        welcomeScreen.style.animation = 'fadeOut 1s forwards';
        setTimeout(() => {
            welcomeScreen.classList.add('hidden');
            mainContent.classList.remove('hidden');
            whatsappIcon.classList.remove('hidden');

            // Animação de entrada das seções
            observeSections();
        }, 500);
    });
    
    // Permitir entrar com a tecla "Enter"
    guestNameInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            enterButton.click();
        }
    });

    // 2. CONTAGEM REGRESSIVA
    const countdownDate = new Date("Dec 27, 2025 12:00:00").getTime();

    const countdownFunction = setInterval(() => {
        const now = new Date().getTime();
        const distance = countdownDate - now;

        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        document.getElementById('days').innerText = String(days).padStart(2, '0');
        document.getElementById('hours').innerText = String(hours).padStart(2, '0');
        document.getElementById('minutes').innerText = String(minutes).padStart(2, '0');
        document.getElementById('seconds').innerText = String(seconds).padStart(2, '0');

        if (distance < 0) {
            clearInterval(countdownFunction);
            document.getElementById('countdown').innerHTML = "A festa começou!";
        }

    }, 1000);
    
    // 3. PLAYLIST NO SPOTIFY
    async function submitMusic(params) {
        
    }


    // 4. ANIMAÇÃO SCROLL (MICRO-INTERAÇÃO)
    const observeSections = () => {
        const sections = document.querySelectorAll('.section-container');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        sections.forEach(section => {
            observer.observe(section);
        });
    };
});