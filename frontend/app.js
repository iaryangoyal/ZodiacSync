const state = {
  token: localStorage.getItem("zodiac_token"),
  user: JSON.parse(localStorage.getItem("zodiac_user") || "null"),
  sessionId: null,
};

const authPanel = document.querySelector("#authPanel");
const chatPanel = document.querySelector("#chatPanel");
const authForm = document.querySelector("#authForm");
const authStatus = document.querySelector("#authStatus");
const chatStatus = document.querySelector("#chatStatus");
const loginTab = document.querySelector("#loginTab");
const registerTab = document.querySelector("#registerTab");
const nameField = document.querySelector("#nameField");
const authSubmit = document.querySelector("#authSubmit");
const userName = document.querySelector("#userName");
const sessionList = document.querySelector("#sessionList");
const messages = document.querySelector("#messages");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");

let authMode = "login";

function setStatus(node, text, isError = false) {
  node.textContent = text;
  node.classList.toggle("error", isError);
}

function setAuthMode(mode) {
  authMode = mode;
  loginTab.classList.toggle("active", mode === "login");
  registerTab.classList.toggle("active", mode === "register");
  nameField.classList.toggle("hidden", mode === "login");
  authSubmit.textContent = mode === "login" ? "Login" : "Create account";
  setStatus(authStatus, "");
}

function headers() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${state.token}`,
  };
}

async function api(path, options = {}) {
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Request failed.");
  }
  return data;
}

function renderShell() {
  const signedIn = Boolean(state.token && state.user);
  authPanel.classList.toggle("hidden", signedIn);
  chatPanel.classList.toggle("hidden", !signedIn);
  if (signedIn) {
    userName.textContent = state.user.full_name;
    loadSessions();
  }
}

function saveAuth(data) {
  state.token = data.access_token;
  state.user = data.user;
  localStorage.setItem("zodiac_token", state.token);
  localStorage.setItem("zodiac_user", JSON.stringify(state.user));
}

function logout() {
  state.token = null;
  state.user = null;
  state.sessionId = null;
  localStorage.removeItem("zodiac_token");
  localStorage.removeItem("zodiac_user");
  messages.innerHTML = "";
  renderShell();
}

function addMessage(role, content) {
  const bubble = document.createElement("div");
  bubble.className = `message ${role}`;
  bubble.textContent = content;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

async function loadSessions() {
  try {
    const sessions = await api("/chat/sessions", { headers: headers() });
    sessionList.innerHTML = "";
    sessions.forEach((session) => {
      const button = document.createElement("button");
      button.className = `session-item ${session.id === state.sessionId ? "active" : ""}`;
      button.textContent = session.title;
      button.type = "button";
      button.addEventListener("click", () => loadMessages(session.id));
      sessionList.appendChild(button);
    });
  } catch (error) {
    setStatus(chatStatus, error.message, true);
  }
}

async function loadMessages(sessionId) {
  state.sessionId = sessionId;
  messages.innerHTML = "";
  const items = await api(`/chat/sessions/${sessionId}/messages`, { headers: headers() });
  items.forEach((item) => addMessage(item.role, item.content));
  await loadSessions();
}

loginTab.addEventListener("click", () => setAuthMode("login"));
registerTab.addEventListener("click", () => setAuthMode("register"));

authForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  setStatus(authStatus, "Working...");
  const payload = {
    email: document.querySelector("#email").value,
    password: document.querySelector("#password").value,
  };
  if (authMode === "register") {
    payload.full_name = document.querySelector("#fullName").value;
  }

  try {
    const data = await api(`/auth/${authMode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    saveAuth(data);
    setStatus(authStatus, "");
    renderShell();
  } catch (error) {
    setStatus(authStatus, error.message, true);
  }
});

document.querySelector("#logoutBtn").addEventListener("click", logout);
document.querySelector("#newChatBtn").addEventListener("click", () => {
  state.sessionId = null;
  messages.innerHTML = "";
  messageInput.focus();
  loadSessions();
});

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  messageInput.value = "";
  addMessage("user", message);
  setStatus(chatStatus, "ZodiacSync is thinking...");

  try {
    const data = await api("/chat", {
      method: "POST",
      headers: headers(),
      body: JSON.stringify({ message, session_id: state.sessionId }),
    });
    state.sessionId = data.session_id;
    addMessage("assistant", data.response);
    setStatus(chatStatus, "");
    await loadSessions();
  } catch (error) {
    setStatus(chatStatus, error.message, true);
  }
});

setAuthMode("login");
renderShell();
