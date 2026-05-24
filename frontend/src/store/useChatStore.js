import { create } from "zustand";

export const useChatStore = create((set, get) => ({

  // =========================
  // 🧠 STATE
  // =========================
  sessions: [],
  currentSessionId: null,

  // 🔥 BACKEND SESSION (IMPORTANT)
  backendSessionId: null,

  // =========================
  // 🆕 CREATE NEW CHAT
  // =========================
  createNewChat: () => {
    const newSession = {
      id: Date.now().toString(),
      messages: [],
      createdAt: new Date(),
      title: "New Chat",
    };

    set((state) => ({
      sessions: [newSession, ...state.sessions],
      currentSessionId: newSession.id,
      backendSessionId: null, // reset AI memory
    }));
  },

  // =========================
  // ➕ ADD MESSAGE
  // =========================
  addMessage: (msg) => {
    let { sessions, currentSessionId } = get();

    // 🔥 AUTO CREATE CHAT
    if (!currentSessionId) {
      const newSession = {
        id: Date.now().toString(),
        messages: [],
        createdAt: new Date(),
        title: "New Chat",
      };

      sessions = [newSession, ...sessions];
      currentSessionId = newSession.id;
    }

    const updatedSessions = sessions.map((session) => {
      if (session.id !== currentSessionId) return session;

      const updatedMessages = [...session.messages, msg];

      // 🔥 AUTO TITLE (first user message only)
      let title = session.title;
      if (session.messages.length === 0 && msg.role === "user") {
        title = msg.content?.slice(0, 30) || "New Chat";
      }

      return {
        ...session,
        messages: updatedMessages,
        title,
      };
    });

    set({
      sessions: updatedSessions,
      currentSessionId,
    });
  },

  // =========================
  // 🔄 SWITCH CHAT
  // =========================
  setCurrentSession: (id) => {
    set({ currentSessionId: id });
  },

  // =========================
  // 📥 GET CURRENT MESSAGES
  // =========================
  getCurrentMessages: () => {
    const { sessions, currentSessionId } = get();

    if (!sessions || sessions.length === 0) return [];

    const session = sessions.find(
      (s) => s.id === currentSessionId
    );

    return session?.messages || [];
  },

  // =========================
  // 🔗 BACKEND SESSION (FIXED)
  // =========================
  setBackendSessionId: (id) => {
    set({ backendSessionId: id });
  },

  getBackendSessionId: () => {
    return get().backendSessionId;
  },

  // =========================
  // ❌ DELETE CHAT
  // =========================
  deleteSession: (id) => {
    const { sessions, currentSessionId } = get();

    const updated = sessions.filter((s) => s.id !== id);

    set({
      sessions: updated,
      currentSessionId:
        currentSessionId === id
          ? updated[0]?.id || null
          : currentSessionId,
    });
  },

}));