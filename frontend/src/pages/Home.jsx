import ChatInput from "../components/ChatInput";
import ChatMessage from "../components/ChatMessage";
import { useChatStore } from "../store/useChatStore";

export default function Home() {

  // ✅ SAFE STATE ACCESS
  const sessions = useChatStore((state) => state.sessions);
  const currentSessionId = useChatStore((state) => state.currentSessionId);

  // ✅ SAFE COMPUTE (NO LOOP)
  const currentSession = sessions.find(
    (s) => s.id === currentSessionId
  );

  const messages = currentSession?.messages || [];

  // 🔥 ADD THIS FUNCTION
  const testProtected = async () => {
    const token = localStorage.getItem("token");

    const res = await fetch("http://localhost:8000/api/auth/protected", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await res.json();
    console.log("Protected Response:", data);
  };

  return (
    <div className="flex-1 flex flex-col bg-[#0B0F19] text-white">

      {messages.length === 0 ? (
        <div className="flex-1 flex flex-col items-center justify-center px-4 text-center">

          <h1 className="text-3xl font-semibold mb-6">
            Hey, Bilal. Ready to dive in?
          </h1>

          {/* 🔥 TEST BUTTON ADD HERE */}
          <button
            onClick={testProtected}
            className="mb-4 px-4 py-2 bg-green-600 rounded hover:bg-green-700"
          >
            Test Protected Route
          </button>

          <div className="w-full max-w-2xl">
            <ChatInput />
          </div>

        </div>
      ) : (
        <div className="flex flex-col flex-1">

          <div className="flex-1 overflow-y-auto space-y-4 py-6 px-4 max-w-3xl w-full mx-auto">
            {messages.map((msg, i) => (
              <ChatMessage key={i} msg={msg} />
            ))}
          </div>

          {/* 🔥 BUTTON YAHAN BHI ADD KAR DIYA */}
          <button
            onClick={testProtected}
            className="mx-auto mb-2 px-4 py-2 bg-green-600 rounded hover:bg-green-700"
          >
            Test Protected Route
          </button>

          <div className="p-4 border-t border-gray-800 max-w-3xl w-full mx-auto">
            <ChatInput />
          </div>

        </div>
      )}

    </div>
  );
}