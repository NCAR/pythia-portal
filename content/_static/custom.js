var buttons = document.querySelectorAll('.modal-btn');
var backdrop = document.querySelector('.backdrop');
var modals = document.querySelectorAll('.modal');
console.log(buttons)
console.log(backdrop)
console.log(modals)

function openModal(i) {
    backdrop.style.display = 'block';
    modals[i].style.display = 'block';
}

function closeModal (i) {
    backdrop.style.display = 'none';
    modals[i].style.display = 'none';
}

for (i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', 
        function(j) {
            return function() {
                openModal(j);
            }
        } (i)
    );
    backdrop.addEventListener('click', 
        function(j) {
            return function() { 
                closeModal(j);
            }
        } (i)
    );
}