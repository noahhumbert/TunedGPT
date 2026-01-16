function scrollToBottom() {
    const chatContainer = document.getElementById("chat-container"); // get fresh element
    if (chatContainer) {
        chatContainer.scrollTo({
            top: chatContainer.scrollHeight,
            behavior: "instant"
        })
    }
}

// Call after DOM loads
window.addEventListener("load", () => {
    scrollToBottom();
});