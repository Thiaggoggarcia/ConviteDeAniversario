document.addEventListener('DOMContentLoaded', () => {
    // ELEMENTOS DO DOM
    const welcomeScreen = document.getElementById('welcome-screen');
    const mainContent = document.getElementById('main-content');
    const guestNameInput = document.getElementById('guest-name-input');
    const enterButton = document.getElementById('enter-button');
    const personalizedGreeting = document.getElementById('personalized-greeting');
    const music = document.getElementById('ambient-music');
    const musicToggle = document.getElementById('music-toggle');
    const messageForm = document.getElementById('message-form');
    const messagesList = document.getElementById('messages-list');

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
        personalizedGreeting.textContent = `${guestName}, o 3.0 não seria o mesmo sem você aqui! 🥂`;
        
        // Transição de telas
        welcomeScreen.style.animation = 'fadeOut 1s forwards';
        setTimeout(() => {
            welcomeScreen.classList.add('hidden');
            mainContent.classList.remove('hidden');
            musicToggle.classList.remove('hidden');
            
            // Iniciar música após interação do usuário
            music.play().catch(error => console.log("A reprodução automática foi bloqueada pelo navegador."));

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

    // 2. CONTROLE DE MÚSICA
    let isPlaying = true;
    musicToggle.addEventListener('click', () => {
        if (isPlaying) {
            music.pause();
            musicToggle.textContent = '🔇';
        } else {
            music.play();
            musicToggle.textContent = '🔊';
        }
        isPlaying = !isPlaying;
    });

    // 3. CONTAGEM REGRESSIVA
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

    // 4. MURAL DE MENSAGENS (COM LOCALSTORAGE)
    const loadMessages = () => {
        const messages = JSON.parse(localStorage.getItem('guestMessages')) || [];
        messagesList.innerHTML = ''; // Limpar lista antes de carregar
        messages.forEach(msg => addMessageToDOM(msg));
    };

    const addMessageToDOM = (msg) => {
        const messageItem = document.createElement('div');
        messageItem.classList.add('message-item');
        
        let messageHTML = `<p class="author">${msg.author}</p><p>"${msg.text}"</p>`;
        if (msg.music) {
            messageHTML += `<p class="music">🎶 Sugestão: ${msg.music}</p>`;
        }
        
        messageItem.innerHTML = messageHTML;
        messagesList.prepend(messageItem); // Adiciona a nova mensagem no topo
    };
    
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const guestName = localStorage.getItem('guestName') || 'Anônimo';
        const messageText = document.getElementById('message-text').value;
        const musicSuggestion = document.getElementById('music-suggestion').value;

        const newMessage = {
            author: guestName,
            text: messageText,
            music: musicSuggestion,
        };

        // Salvar no localStorage
        const messages = JSON.parse(localStorage.getItem('guestMessages')) || [];
        messages.push(newMessage);
        localStorage.setItem('guestMessages', JSON.stringify(messages));

        addMessageToDOM(newMessage);

        // Limpar formulário
        messageForm.reset();
    });

    // Carregar mensagens existentes ao iniciar
    loadMessages();

    // 5. ANIMAÇÃO SCROLL (MICRO-INTERAÇÃO)
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