import { useState } from "react";
import { useChatStore } from "../store/useChatStore";

export default function Sidebar() {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");

  // ✅ Zustand SAFE SELECTORS
  const sessions = useChatStore((state) => state.sessions) || [];
  const createNewChat = useChatStore((state) => state.createNewChat);
  const setCurrentSession = useChatStore((state) => state.setCurrentSession);
  const currentSessionId = useChatStore((state) => state.currentSessionId);

  // 🔍 FILTER LOGIC
  const filtered = sessions.filter((s) => {
    if (!search) return true;

    return s.messages?.some((m) =>
      m.content?.toLowerCase().includes(search.toLowerCase())
    );
  });

  return (
    <div className="w-72 bg-[#0B0F19] text-white p-4 flex flex-col">

      {/* 🔥 NEW CHAT */}
      <div
        onClick={createNewChat}
        className="p-2 rounded hover:bg-gray-800 cursor-pointer mb-2"
      >
        + New chat
      </div>

      {/* 🔍 SEARCH */}
      <input
        placeholder="Search chats..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full p-2 bg-gray-800 rounded mb-3 outline-none"
      />

      {/* 📁 MENU */}
      <div className="space-y-2">

        <div className="p-2 rounded hover:bg-gray-800 cursor-pointer">
          Projects
        </div>

        <div className="p-2 rounded hover:bg-gray-800 cursor-pointer">
          Codex
        </div>

        <div
          onClick={() => setOpen(!open)}
          className="p-2 rounded hover:bg-gray-800 cursor-pointer"
        >
          ⋯ More
        </div>

        {open && (
          <div className="bg-gray-800 rounded-lg p-2 ml-2 space-y-2 shadow-lg">
            <div className="hover:bg-gray-700 p-2 rounded">Images</div>
            <div className="hover:bg-gray-700 p-2 rounded">Deep research</div>
            <div className="hover:bg-gray-700 p-2 rounded">Apps</div>
          </div>
        )}
      </div>

      {/* 💬 CHAT LIST */}
      <div className="mt-4 flex-1 overflow-y-auto space-y-2">

        {filtered.length === 0 ? (
          <p className="text-gray-500 text-sm">No chats</p>
        ) : (
          filtered.map((session) => (
            <div
              key={session.id}
              onClick={() => setCurrentSession(session.id)}
              className={`p-2 rounded cursor-pointer truncate ${
                currentSessionId === session.id
                  ? "bg-gray-700"
                  : "bg-gray-800 hover:bg-gray-700"
              }`}
            >
              {session.messages?.[0]?.content || "New Chat"}
            </div>
          ))
        )}

      </div>

    </div>
  );
}