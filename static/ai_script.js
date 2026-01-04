document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('user_prompt');
    const form = document.getElementById('chat-form');
    const popup = document.getElementById('popup');
    const backdrop = document.getElementById('backdrop');
    const userPrompt = document.getElementById('user_prompt');
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const chatContainer = document.getElementById('messages-container');
    const chatModelButton = document.querySelector('.model-button');
    const chatModelOptions = document.querySelector('.chat-model-options');
    const chatModel = document.querySelector('.chat-model');
    const modelButton = document.getElementById('model-button');
    const modelOptionInput = document.getElementById('model_option');

    // Toggle dropdown menu
    hamburgerMenu.addEventListener('click', function() {
        dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
    });

    // Adjust textarea height
    function adjustHeight() {
        textarea.style.height = 'auto'; // Reset height to fit content
        textarea.style.height = textarea.scrollHeight + 'px'; // Set height to scroll height
    }

    textarea.addEventListener('input', adjustHeight); // Adjust on input
    adjustHeight(); // Initial adjustment

    // Scroll to bottom of messages container on form submission
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission
        popup.style.display = 'block'; // Show the popup
        backdrop.style.display = 'block';

        form.submit(); // Submit the form after hiding the popup
    });

    userPrompt.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default form submission
            popup.style.display = 'block'; // Show the popup
            backdrop.style.display = 'block';

            form.submit(); // Submit the form after hiding the popup
        }
    });

    setTimeout(function() {
        var height = chatContainer.scrollHeight;
        chatContainer.scroll(0, height);
    }, 200);
    
    chatModelButton.addEventListener('click', function () {
        chatModel.classList.toggle('show');
    });

    chatModelOptions.addEventListener('click', function (event) {
        if (event.target.tagName === 'BUTTON') {
            chatModelButton.textContent = event.target.textContent;
            chatModel.classList.remove('show');
        }
    });

    form.addEventListener('submit', function(event) {
        if (!userPrompt.value.trim()) {
            event.preventDefault(); // Prevent form submission if textarea is empty
        }
    });

    // Set default value on page load
    const defaultOption = document.querySelector('.dropdown-option[aria-selected="true"]');
    if (defaultOption) {
        modelButton.textContent = defaultOption.textContent;
        modelOptionInput.value = defaultOption.getAttribute('data-value');
    }

    // Handle option selection
    document.querySelectorAll('.dropdown-option').forEach(button => {
        button.addEventListener('click', function() {
            // Update button text
            modelButton.textContent = this.textContent;

            // Update hidden input value
            modelOptionInput.value = this.getAttribute('data-value');

            // Update aria-selected attribute
            document.querySelectorAll('.dropdown-option').forEach(opt => opt.setAttribute('aria-selected', 'false'));
            this.setAttribute('aria-selected', 'true');
        });
    });
});
