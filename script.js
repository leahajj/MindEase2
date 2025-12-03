
// -----------------------------
// NAVIGATION
// -----------------------------
function goTo(page) {
    window.location.href = page;
}



// -----------------------------
// CHATBOT
// -----------------------------
function sendMessage() {
    const input = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");

    if (!input || !chatBox) return;

    const userMessage = input.value.trim();
    if (!userMessage) return;

    // user bubble
    const userDiv = document.createElement("div");
    userDiv.classList.add("user-bubble");
    userDiv.textContent = userMessage;
    chatBox.appendChild(userDiv);

    // bot bubble
    const botDiv = document.createElement("div");
    botDiv.classList.add("bot-bubble");
    botDiv.textContent = getBotReply(userMessage);
    chatBox.appendChild(botDiv);

    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;
}

function getBotReply(message) {
    const lower = message.toLowerCase();

    if (lower.includes("recommend")) {
        getRecommendations(2); // default mood score
        return "Let me get some recommendations for you…";
    }

    if (lower.includes("hi") || lower.includes("hello"))
        return "Hi! How are you feeling today?";

    if (lower.includes("sad"))
        return "I'm sorry you're feeling that way 💙";

    if (lower.includes("happy"))
        return "That's great to hear 🌟";

    return "I'm here for you — tell me more.";
}

function openEndChatPopup() { document.getElementById("endChatPopup").style.display = "flex"; }
function closeEndChatPopup() { document.getElementById("endChatPopup").style.display = "none"; }
function openSaveChatPopup() { document.getElementById("saveChatPopup").style.display = "flex"; }
function closeSaveChatPopup() { document.getElementById("saveChatPopup").style.display = "none"; }



// -----------------------------
// MOOD LOGGER (8000)
// -----------------------------
function logMood() {
    const mood = document.getElementById("moodInput").value;
    const journal = document.getElementById("journalInput").value;
    const date = new Date().toISOString().split("T")[0];

    fetch("http://127.0.0.1:8000/log_mood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            user_id: "test1",
            mood: mood,
            date: date,
            journal_text: journal
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("logResult").innerText = "Mood saved!";
        loadDailySummary();
        loadWeeklySummary();
    })
    .catch(err => console.error("Error logging mood:", err));
}



// -----------------------------
// DAILY SUMMARY (8001)
// -----------------------------
function loadDailySummary() {
    const today = new Date().toISOString().split("T")[0];

    fetch(`http://127.0.0.1:8001/daily_summary?user_id=test1&date=${today}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("dailySummary").innerText =
                `Today's Summary:\nEntries: ${data.entries_today}\nAverage Mood: ${data.average_today}`;
        })
        .catch(err => console.error("Error loading daily summary:", err));
}



// -----------------------------
// WEEKLY SUMMARY (8001)
// -----------------------------
function loadWeeklySummary() {
    fetch("http://127.0.0.1:8001/weekly_summary?user_id=test1")
        .then(res => res.json())
        .then(data => {
            document.getElementById("weeklySummary").innerText =
                `Weekly Summary:\nEntries: ${data.entries_week}\nAverage Mood: ${data.weekly_average}`;
        })
        .catch(err => console.error("Error loading weekly summary:", err));
}



// -----------------------------
// TREND ANALYSIS (8002)
// -----------------------------
function loadTrend() {
    fetch("http://127.0.0.1:8002/trend?user_id=test1")
        .then(res => res.json())
        .then(data => {
            document.getElementById("trendResult").innerText =
                `Mood Trend: ${data.trend}`;
        })
        .catch(err => console.error("Error loading trend:", err));
}



// -----------------------------
// RECOMMENDATIONS (8003)
// -----------------------------
function getRecommendations(score) {
    fetch("http://127.0.0.1:8003/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mood_score: score })
    })
    .then(res => res.json())
    .then(data => {
        const chatBox = document.getElementById("chatBox");

        const botDiv = document.createElement("div");
        botDiv.classList.add("bot-bubble");
        botDiv.innerHTML = `
            <strong>Recommendations:</strong><br>
            ${data.coping_strategies.join("<br>")}
            <br><br><strong>OSU Resources:</strong><br>
            ${data.osu_resources.join("<br>")}
        `;

        chatBox.appendChild(botDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(err => console.error("Error loading recommendations:", err));
}

  .catch(err => console.error(err));
}
