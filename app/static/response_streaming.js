document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const userSpan = document.getElementById("user-message");
    const userContainer = document.getElementById("user-message-container");
    const aiSpan = document.getElementById("live-response");
    const aiContainer = document.getElementById("ai-message-container");

    const chatContainer = document.getElementById("chat-container");

    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // needed for streaming

        const messageInput = form.querySelector('input[name="message"]');
        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        // Show placeholders and insert user message
        userSpan.style.display = "inline";
        userSpan.textContent = userMessage;
        userContainer.hidden = false;

        aiSpan.style.display = "inline";
        aiSpan.textContent = "";
        aiContainer.hidden = false;

        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Start streaming
        const response = await fetch("/", {
            method: "POST",
            body: new FormData(form)
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            aiSpan.textContent += decoder.decode(value, { stream: true });
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        // Once done, hide placeholders again
        userSpan.style.display = "none";
        userContainer.hidden = true;
        aiSpan.style.display = "none";
        aiContainer.hidden = true;

        form.reset();

        fetch("/")
            .then(res => res.text())
            .then(html => {
                // Replace the current page
                document.open();
                document.write(html);
                document.close();

                // Wait for the DOM to fully load
                window.requestAnimationFrame(() => {
                    // scroll_bottom.js defines this function globally
                    if (typeof scrollToBottom === "function") {
                        scrollToBottom();
                    }
                });
            });
    });
});
