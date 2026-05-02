(function () {
  "use strict";

  var toggleButton = document.getElementById("chat-toggle");
  var closeButton = document.getElementById("chat-close");
  var panel = document.getElementById("chat-panel");
  var form = document.getElementById("chat-form");
  var input = document.getElementById("chat-input");
  var messages = document.getElementById("chat-messages");

  if (!toggleButton || !closeButton || !panel || !form || !input || !messages) {
    return;
  }

  var starterMessages = [
    "Hi, this is ServiceCall AI demo chat. How can we help with your comfort issue today?",
    "Try asking about A/C repair, water heater replacement, or scheduling options.",
  ];

  function appendMessage(role, text) {
    var node = document.createElement("p");
    node.className = "message " + role;
    node.textContent = text;
    messages.appendChild(node);
    messages.scrollTop = messages.scrollHeight;
  }

  function appendAssistantPlaceholder(userText) {
    var response = "Placeholder response: thanks for your message about \"" + userText +
      "\". In a later milestone this will route to the FastAPI and RAG backend.";
    appendMessage("assistant", response);
  }

  function setOpenState(isOpen) {
    panel.classList.toggle("open", isOpen);
    panel.setAttribute("aria-hidden", String(!isOpen));
    toggleButton.setAttribute("aria-expanded", String(isOpen));
    if (isOpen) {
      input.focus();
    }
  }

  function recordOutcomeEvent(eventType, details) {
    var outcome = {
      eventType: eventType,
      details: details,
      source: "static-site-shell",
      timestamp: new Date().toISOString(),
    };
    console.log("outcome_event", outcome);
  }

  starterMessages.forEach(function (message) {
    appendMessage("assistant", message);
  });
  recordOutcomeEvent("chat_loaded", "starter_messages_rendered");

  toggleButton.addEventListener("click", function () {
    setOpenState(!panel.classList.contains("open"));
    recordOutcomeEvent("chat_toggled", panel.classList.contains("open") ? "opened" : "closed");
  });

  closeButton.addEventListener("click", function () {
    setOpenState(false);
    recordOutcomeEvent("chat_toggled", "closed_from_panel");
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var text = input.value.trim();
    if (!text) {
      return;
    }
    appendMessage("user", text);
    appendAssistantPlaceholder(text);
    input.value = "";
    recordOutcomeEvent("chat_message_submitted", "placeholder_response_appended");
  });
})();
