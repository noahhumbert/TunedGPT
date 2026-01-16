const chatContainer = document.getElementById("chat-container");

function scrollToBottom() {
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Call after DOM loads
document.addEventListener("DOMContentLoaded", () => {
    scrollToBottom();
});

// Call after adding new message or streaming chunk
scrollToBottom();
