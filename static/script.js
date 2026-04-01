const elements = {
    chatbox: document.getElementById("chatbox"),
    input: document.getElementById("message"),
    sendBtn: document.getElementById("send-btn"),
    typingIndicator: document.getElementById("typing-indicator"),
    themeToggleGrp: document.getElementById("theme-toggle"),
    themeIcon: document.getElementById("theme-icon")
};

// ==========================================
// Theme Toggling Logic
// ==========================================
// 1. Check local storage or default to 'dark'
const currentTheme = localStorage.getItem("theme") || "dark";
document.documentElement.setAttribute("data-theme", currentTheme);
updateThemeIcon(currentTheme);

elements.themeToggleGrp.addEventListener("click", () => {
    let theme = document.documentElement.getAttribute("data-theme");
    
    // Switch to opposite
    let newTheme = theme === "dark" ? "light" : "dark";
    
    // Apply
    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateThemeIcon(newTheme);
});

function updateThemeIcon(theme) {
    if (theme === "light") {
        elements.themeIcon.className = "ph-fill ph-moon"; // Show moon in light mode
    } else {
        elements.themeIcon.className = "ph-fill ph-sun"; // Show sun in dark mode
    }
}

// ==========================================
// Chat Logic
// ==========================================
elements.input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function scrollToBottom() {
    elements.chatbox.scrollTop = elements.chatbox.scrollHeight;
}

function appendMessage(sender, text, isError = false, recommendations = null) {
    const isUser = sender === "user";
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${isUser ? 'user' : 'bot'}`;
    
    const iconClass = isUser ? 'ph-user' : 'ph-robot';
    let contentHtml = `<p class="${isError ? 'error-text' : ''}">${text}</p>`;
    
    if (recommendations && recommendations.length > 0) {
        contentHtml += `<ul>`;
        recommendations.forEach(r => {
            contentHtml += `<li>🎬 ${r}</li>`;
        });
        contentHtml += `</ul>`;
    }

    msgDiv.innerHTML = `
        <div class="avatar"><i class="ph ${iconClass}"></i></div>
        <div class="msg-content">
            ${contentHtml}
        </div>
    `;

    elements.chatbox.appendChild(msgDiv);
    // Tiny delay to ensure DOM render before scrolling
    setTimeout(scrollToBottom, 50);
}

async function sendMessage() {
    const message = elements.input.value.trim();
    if (!message) return;

    // 1. Display User Message
    appendMessage("user", message);
    
    // 2. Loading State
    elements.input.value = "";
    elements.input.disabled = true;
    elements.sendBtn.disabled = true;
    elements.typingIndicator.classList.remove("hidden");
    scrollToBottom();

    // 3. API Transaction
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.error) {
            appendMessage("bot", data.reply, true);
        } else {
            appendMessage("bot", data.reply, false, data.recommendations);
        }
    } catch (error) {
        console.error("Chatbot Network Error:", error);
        appendMessage("bot", "Oops! I couldn't reach the backend API. Please restart your python server.", true);
    } finally {
        elements.typingIndicator.classList.add("hidden");
        elements.input.disabled = false;
        elements.sendBtn.disabled = false;
        elements.input.focus();
        scrollToBottom();
    }
}