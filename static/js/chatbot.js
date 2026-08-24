/**
 * chatbot.js — Interactive client-side logic for AI Health Chatbot
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatContainer = document.getElementById('chatContainer');
  const sendBtn = document.getElementById('sendBtn');
  const clearBtn = document.getElementById('clearChatBtn');
  const quickPrompts = document.querySelectorAll('.quick-prompt');

  // Handle Quick Prompts
  quickPrompts.forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-text');
      chatInput.value = text;
      chatInput.focus();
    });
  });

  // Handle Clear Chat
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      chatContainer.innerHTML = `
        <div class="chat-bubble chat-bubble-ai">
          <div class="d-flex align-items-center gap-2 mb-1">
            <i class="fa-solid fa-robot text-info"></i>
            <strong class="small text-info">AI Health Assistant</strong>
          </div>
          <p class="mb-0">Chat cleared! How else can I assist you with your health today?</p>
        </div>
      `;
    });
  }

  // Handle Chat Submit
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Append User Bubble
    appendMessage(userMessage, 'user');
    chatInput.value = '';
    chatInput.disabled = true;
    sendBtn.disabled = true;

    // Show Typing Indicator
    const typingId = showTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      removeTypingIndicator(typingId);

      if (data.response) {
        appendMessage(data.response, 'ai', data.is_emergency);
      } else {
        appendMessage("I'm sorry, I couldn't process your request right now. Please try again.", 'ai');
      }
    } catch (err) {
      removeTypingIndicator(typingId);
      appendMessage("⚠️ Connection error. Please check your network and try again.", 'ai');
    } finally {
      chatInput.disabled = false;
      sendBtn.disabled = false;
      chatInput.focus();
    }
  });

  function appendMessage(text, sender, isEmergency = false) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender === 'user' ? 'chat-bubble-user' : 'chat-bubble-ai'}`;

    if (isEmergency) {
      bubble.classList.add('chat-bubble-emergency');
    }

    if (sender === 'user') {
      bubble.innerHTML = `
        <div class="d-flex align-items-center justify-content-end gap-2 mb-1">
          <span class="small opacity-75">You</span>
          <i class="fa-solid fa-user"></i>
        </div>
        <div>${escapeHtml(text)}</div>
      `;
    } else {
      // Format markdown-like bold and bullet lists in simple text
      const formatted = formatText(text);
      bubble.innerHTML = `
        <div class="d-flex align-items-center gap-2 mb-1">
          <i class="fa-solid fa-robot ${isEmergency ? 'text-danger' : 'text-info'}"></i>
          <strong class="small ${isEmergency ? 'text-danger' : 'text-info'}">
            ${isEmergency ? 'EMERGENCY ALERT' : 'AI Health Assistant'}
          </strong>
        </div>
        <div class="chat-content">${formatted}</div>
      `;
    }

    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    const indicator = document.createElement('div');
    indicator.id = id;
    indicator.className = 'chat-bubble chat-bubble-ai py-2 px-3 text-secondary small d-flex align-items-center gap-2';
    indicator.innerHTML = `
      <i class="fa-solid fa-circle-notch fa-spin text-info"></i>
      <span>Analyzing health response...</span>
    `;
    chatContainer.appendChild(indicator);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return id;
  }

  function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function formatText(str) {
    return str
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>');
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
  }
});
