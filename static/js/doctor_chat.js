/**
 * doctor_chat.js — Handles sending and polling live doctor-patient consultation messages
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('doctorChatForm');
  const input = document.getElementById('doctorMessageInput');
  const sendBtn = document.getElementById('sendDoctorMsgBtn');
  const container = document.getElementById('doctorChatContainer');
  const placeholder = document.getElementById('emptyChatPlaceholder');

  const patientId = document.getElementById('chatPatientId')?.value;
  const doctorId = document.getElementById('chatDoctorId')?.value;
  const senderType = document.getElementById('chatSenderType')?.value;

  if (!form || !patientId || !doctorId) return;

  // Scroll to bottom on load
  container.scrollTop = container.scrollHeight;

  // Handle message sending
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    input.disabled = true;
    sendBtn.disabled = true;

    try {
      const res = await fetch('/api/doctor-chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: parseInt(patientId),
          doctor_id: parseInt(doctorId),
          sender_type: senderType,
          message: text
        })
      });

      const data = await res.json();
      if (data.success) {
        if (placeholder) placeholder.remove();

        const bubble = document.createElement('div');
        bubble.className = 'chat-bubble chat-bubble-user';
        bubble.innerHTML = `
          <div class="d-flex align-items-center gap-2 mb-1">
            <strong class="small">${senderType === 'doctor' ? '<i class="fa-solid fa-user-doctor me-1"></i> Doctor (You)' : '<i class="fa-solid fa-user me-1"></i> You'}</strong>
            <span class="text-muted ms-auto" style="font-size: 11px;">${data.date_time}</span>
          </div>
          <div>${escapeHtml(text)}</div>
        `;
        container.appendChild(bubble);
        container.scrollTop = container.scrollHeight;
        input.value = '';
      }
    } catch (err) {
      console.error("Message send error:", err);
    } finally {
      input.disabled = false;
      sendBtn.disabled = false;
      input.focus();
    }
  });

  // Polling for new messages every 4 seconds
  setInterval(async () => {
    try {
      const res = await fetch(`/api/doctor-chat/messages/${patientId}/${doctorId}`);
      const messages = await res.json();
      if (messages && messages.length > 0) {
        if (placeholder) placeholder.remove();

        // Render entire list cleanly if count increased
        const currentCount = container.querySelectorAll('.chat-bubble').length;
        if (messages.length > currentCount) {
          container.innerHTML = '';
          messages.forEach(msg => {
            const isUser = (senderType === msg.sender_type);
            const bubble = document.createElement('div');
            bubble.className = `chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-doctor'}`;
            bubble.innerHTML = `
              <div class="d-flex align-items-center gap-2 mb-1">
                <strong class="small">
                  ${msg.sender_type === 'doctor' ? '<i class="fa-solid fa-user-doctor me-1"></i> Doctor' : '<i class="fa-solid fa-user me-1"></i> Patient'}
                </strong>
                <span class="text-muted ms-auto" style="font-size: 11px;">${msg.date_time}</span>
              </div>
              <div>${escapeHtml(msg.message)}</div>
            `;
            container.appendChild(bubble);
          });
          container.scrollTop = container.scrollHeight;
        }
      }
    } catch (e) {
      // Ignore polling errors
    }
  }, 4000);

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.innerText = text;
    return div.innerHTML;
  }
});
