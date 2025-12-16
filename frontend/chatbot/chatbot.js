const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");

function cleanMarkdown(text) {
  return text
    .replace(/^#{1,6}\s*/gm, "")
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/^-{3,}$/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function addMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.innerText = cleanMarkdown(text);
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  const thinkingMsg = document.createElement("div");
  thinkingMsg.className = "message bot";
  thinkingMsg.innerText = "Thinking...";
  chatMessages.appendChild(thinkingMsg);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  try {
    const res = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    chatMessages.removeChild(thinkingMsg);

    addMessage(
      data.reply || "Sorry, I couldn't understand.",
      "bot"
    );

  } catch (error) {
    chatMessages.removeChild(thinkingMsg);
    addMessage("Server error. Please try again.", "bot");
  }
}
