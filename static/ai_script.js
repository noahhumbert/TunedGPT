document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('user_prompt');
    const form = document.getElementById('chat-form');
    const popup = document.getElementById('popup');
    const backdrop = document.getElementById('backdrop');
    const userPrompt = document.getElementById('user_prompt');
    const hamburgerMenu = document.querySelector('.hamburger-menu');
    const dropdownMenu = document.getElementById('dropdown-menu');
    
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

        // Simulate AI processing time
        setTimeout(() => {
            popup.style.display = 'none'; // Hide the popup
            backdrop.style.display = 'none';
            form.submit(); // Submit the form after hiding the popup
        }, 2000); // Adjust the time as needed
    });

    userPrompt.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default form submission
            popup.style.display = 'block'; // Show the popup
            backdrop.style.display = 'block';
        }
    });
});
