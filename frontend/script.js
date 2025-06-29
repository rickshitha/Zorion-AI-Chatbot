const chatbox = document.getElementById('chatbox');
const input = document.getElementById('userInput');

function addMessage(sender, text, isMarkdown = false) {
  const msg = document.createElement('div');
  msg.classList.add('message', sender);
  
  if (isMarkdown) {
    msg.innerHTML = marked.parse(text); // ✅ render Markdown as HTML
  } else {
    msg.innerText = text;
  }

  chatbox.appendChild(msg);
  chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage() {
  const text = input.value;
  if (!text.trim()) return;

  const placeholder = document.getElementById('bot-placeholder');
  if (placeholder) placeholder.remove();

  addMessage('user', text);
  input.value = '';

  // Placeholder loading message
  addMessage('bot', 'Typing...');

  // Replace with real API call to Gemini later
  const response = await fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: text })
  });

  const data = await response.json();

  // Replace the last "Typing..." message with actual reply (Markdown parsed)
  const lastBot = document.querySelector('.bot:last-child');
  lastBot.innerHTML = marked.parse(data.reply);
}
