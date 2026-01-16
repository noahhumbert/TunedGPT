function scrollToBottom() {
    const chatContainer = document.getElementById("chat-container"); // get fresh element
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Call after DOM loads
document.addEventListener("DOMContentLoaded", () => {
    scrollToBottom();
});
