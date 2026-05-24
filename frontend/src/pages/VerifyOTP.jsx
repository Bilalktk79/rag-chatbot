import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function VerifyOTP() {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();

  const handleVerify = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/api/auth/verify-otp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, otp })
    });

    const data = await res.json();

    if (data?.message) {
      alert("Verified successfully ✅");
      navigate("/");
    } else {
      alert(data?.error || "Invalid OTP ❌");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h2 className="text-xl mb-4">Verify OTP</h2>

      <form onSubmit={handleVerify} className="space-y-3">

        <input
          type="email"
          placeholder="Enter Email"
          className="p-2 border"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="text"
          placeholder="Enter OTP"
          className="p-2 border"
          onChange={(e) => setOtp(e.target.value)}
        />

        <button className="bg-blue-500 text-white px-4 py-2">
          Verify
        </button>

      </form>
    </div>
  );
}