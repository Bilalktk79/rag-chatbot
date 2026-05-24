import { useState, useRef } from "react";
import { useChatStore } from "../store/useChatStore";
import { sendMessage } from "../services/api";

export default function ChatInput() {
  const [text, setText] = useState("");
  const fileRef = useRef(null);

  // ✅ STORE
  const { addMessage, backendSessionId, setBackendSessionId } = useChatStore();

  // =========================
  // 💬 SEND MESSAGE
  // =========================
  const handleSend = async () => {
    console.log("🔥 BUTTON CLICKED");

    const messageToSend = text.trim();

    if (!messageToSend) {
      console.log("❌ EMPTY INPUT");
      return;
    }

    console.log("📤 Sending:", messageToSend);

    // 👤 show user message instantly
    addMessage({ role: "user", content: messageToSend });

    setText("");

    try {
      console.log("📡 API CALL START");

      const res = await sendMessage({
        message: messageToSend,
        session_id: backendSessionId || null,
      });

      console.log("✅ FULL API RESPONSE:", res);

      // 🔥 SMART RESPONSE HANDLING (FIX)
      const aiReply = res?.response || res?.answer;

      if (!aiReply) {
        addMessage({
          role: "assistant",
          content: "⚠️ Empty response from backend",
        });
        return;
      }

      console.log("STORE ADD:", aiReply);

      // 🤖 AI response
      addMessage({
        role: "assistant",
        content: aiReply,
      });

      // 🧠 SAVE SESSION
      if (!backendSessionId && res.session_id) {
        setBackendSessionId(res.session_id);
        console.log("🧠 Session saved:", res.session_id);
      }

    } catch (err) {
      console.error("❌ FETCH ERROR:", err);

      addMessage({
        role: "assistant",
        content: "Server error ❌",
      });
    }
  };

  // =========================
  // 📁 FILE UPLOAD
  // =========================
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const allowedTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "text/plain",
    ];

    if (!allowedTypes.includes(file.type)) {
      addMessage({
        role: "assistant",
        content: "❌ Only PDF, DOC, DOCX, TXT allowed",
      });
      return;
    }

    addMessage({
      role: "user",
      content: `📎 Uploading: ${file.name}`,
    });

    const formData = new FormData();
    formData.append("file", file);

    try {
      console.log("📡 Uploading file...");

      const res = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      console.log("✅ Upload response:", data);

      addMessage({
        role: "assistant",
        content: `✅ File processed: ${file.name}`,
      });

    } catch (err) {
      console.error("❌ Upload error:", err);

      addMessage({
        role: "assistant",
        content: "❌ File upload failed",
      });
    }
  };

  return (
    <div className="flex items-center bg-[#1E293B] rounded-full px-4 py-2 shadow-lg border border-gray-700">

      {/* ➕ FILE BUTTON */}
      <button
        onClick={() => fileRef.current.click()}
        className="text-gray-400 mr-2 text-lg hover:text-white transition"
        title="Upload file"
      >
        +
      </button>

      {/* HIDDEN INPUT */}
      <input
        type="file"
        ref={fileRef}
        onChange={handleFileUpload}
        className="hidden"
      />

      {/* TEXT INPUT */}
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Ask anything"
        className="flex-1 bg-transparent outline-none text-white placeholder-gray-400"
      />

      {/* SEND BUTTON */}
      <button
        onClick={handleSend}
        className="ml-2 bg-green-500 hover:bg-green-600 transition px-4 py-1 rounded-full text-white"
      >
        →
      </button>

    </div>
  );
}