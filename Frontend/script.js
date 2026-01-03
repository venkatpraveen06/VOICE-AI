async function sendMessage() {
  const input = document.getElementById("textInput");
  if (!input.value) return;

  addMessage(input.value, "user");
  const aiDiv = document.createElement("div");
  aiDiv.className = "message ai";
  messages.appendChild(aiDiv);

  const res = await fetch("http://127.0.0.1:5000/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: input.value })
  });

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    aiDiv.textContent += decoder.decode(value);
    messages.scrollTop = messages.scrollHeight;
  }

  input.value = "";
}
