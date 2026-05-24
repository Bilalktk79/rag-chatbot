export default function ChatMessage({ msg }) {
  return (
    <div
      className={`p-3 rounded max-w-xl ${
        msg.role === "user"
          ? "bg-green-600 ml-auto"
          : "bg-gray-700"
      }`}
    >
      {msg.content}   {/* 🔥 FIXED */}
    </div>
  );
}