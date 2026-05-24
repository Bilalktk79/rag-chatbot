const API = "http://localhost:8000";

// ================= AUTH =================
export const signupUser = async (data) => {
  try {
    const res = await fetch(`${API}/api/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const json = await res.json();
    console.log("SIGNUP RESPONSE:", json);

    return json;

  } catch (err) {
    console.error("Signup Error:", err);
    return { error: "Signup failed" };
  }
};

export const loginUser = async (data) => {
  try {
    const res = await fetch(`${API}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const json = await res.json();

    console.log("LOGIN RESPONSE:", json);

    // 🔥 SAVE TOKEN
    if (json?.token) {
      localStorage.setItem("token", json.token);
      console.log("✅ TOKEN SAVED:", json.token);
    } else {
      console.warn("❌ NO TOKEN RECEIVED");
    }

    return json;

  } catch (err) {
    console.error("Login Error:", err);
    return { error: "Login failed" };
  }
};

// ================= CHAT =================
export const sendMessage = async (data) => {
  try {
    const token = localStorage.getItem("token");

    console.log("📤 TOKEN:", token);

    if (!token) {
      console.error("❌ TOKEN MISSING");
      return { error: "Unauthorized (No token)" };
    }

    const res = await fetch(`${API}/api/chat`, {   // ✅ NO slash
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`   // 🔥 REQUIRED
      },
      body: JSON.stringify(data),
    });

    console.log("📡 STATUS:", res.status);

    // 🔥 HANDLE 401
    if (res.status === 401) {
      console.error("❌ UNAUTHORIZED - TOKEN ISSUE");
      return { error: "Unauthorized ❌" };
    }

    const json = await res.json();

    console.log("✅ API RESPONSE:", json);

    return json;

  } catch (err) {
    console.error("API ERROR:", err);
    return { error: "Server unreachable" };
  }
};

// ================= CHAT HISTORY (OLD) =================
export const getChats = async (sessionId) => {
  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API}/api/chat/${sessionId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    return await res.json();

  } catch (err) {
    console.error("Fetch Chats Error:", err);
    return [];
  }
};

// ================= 🔥 USER CHAT HISTORY =================
export const getUserChats = async () => {
  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API}/api/chat/history`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    return await res.json();

  } catch (err) {
    console.error("Fetch User Chats Error:", err);
    return [];
  }
};

// ================= 🔥 DELETE CHAT =================
export const deleteChat = async (sessionId) => {
  try {
    const token = localStorage.getItem("token");

    const res = await fetch(`${API}/api/chat/delete/${sessionId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    return await res.json();

  } catch (err) {
    console.error("Delete Chat Error:", err);
    return { error: "Delete failed" };
  }
};