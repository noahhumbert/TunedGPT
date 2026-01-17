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

        const modeSelect = form.querySelector('select[name="mode-select"]');
        const mode = modeSelect.value;

        // Show placeholders and insert user message
        userSpan.style.display = "inline";
        userSpan.textContent = userMessage;
        userContainer.hidden = false;

        aiSpan.style.display = "inline";
        aiSpan.textContent = "";
        aiContainer.hidden = false;
        generatedImg.style.display = "none";
        generatedImg.src = "";
        downloadBtn.style.display = "none";

        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        if (mode === "imagegen") {
            // --- Image generation ---
            const response = await fetch("/", {
                method: "POST",
                body: new URLSearchParams({ message: userMessage, "mode-select": mode })
            });

            if (!response.ok) {
                alert("Image generation failed.");
                return;
            }

            const blob = await response.blob();
            const imgUrl = URL.createObjectURL(blob);

            generatedImg.src = imgUrl;
            generatedImg.style.display = "block";

            // Optional: add download button
            downloadBtn.style.display = "inline-block";
            downloadBtn.onclick = () => {
                const a = document.createElement("a");
                a.href = imgUrl;
                a.download = "generated.png";
                a.click();
            };
        }
        else {
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

            fetch("/").then(res => res.text()).then(html => {
                document.open();
                document.write(html);
                document.close();
            });
        }
    });
});
