document.addEventListener('DOMContentLoaded', (event) => {
    const forms = document.querySelectorAll('form');
    forms.forEach((form, index) => {
        form.style.animationDelay = `${index * 0.2}s`;
    });

    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 100);
        });
    });

    // Ajustement de la position du singe en fonction de la largeur de la fenêtre
    const monkey = document.querySelector('.jumping-monkey');
    function adjustMonkeyPosition() {
        const windowWidth = window.innerWidth;
        const monkeyWidth = 100; // La largeur du singe en pixels
        const maxLeft = windowWidth - monkeyWidth;
        monkey.style.maxWidth = `${maxLeft}px`;
    }

    // Appliquer l'ajustement au chargement et au redimensionnement de la fenêtre
    adjustMonkeyPosition();
    window.addEventListener('resize', adjustMonkeyPosition);
});