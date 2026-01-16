function scrollToBottom() {
    const chatContainer = document.getElementById("chat-container"); // get fresh element
    if (chatContainer) {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: "smooth"
        })
    }
}

// Call after DOM loads
window.addEventListener("load", () => {
        const chatContainer = document.getElementById("chat-container");
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    });