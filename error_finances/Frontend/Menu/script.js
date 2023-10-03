// script.js
document.addEventListener("DOMContentLoaded", function() {
    var toggleButton = document.getElementById('toggleButton');
    var Container = document.querySelector('.container');
    var rightContainer = document.querySelector('.right-container');


    toggleButton.addEventListener('click', function() {
        if (Container.style.display === 'none' || Container.style.display === '') {
            Container.style.display = 'flex';
            
            rightContainer.style.marginLeft = '282px';  // Define a margem à esquerda como 25px
        } else {
            Container.style.display = 'none';
            rightContainer.style.marginLeft = '0px';
            // Reseta a margem à esquerda para 0px
        }
    });
});
