import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { signupUser } from "../../services/api";

// ICONS
import { FcGoogle } from "react-icons/fc";
import { FaFacebookF, FaLinkedinIn } from "react-icons/fa";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();

    if (!name || !email || !password) {
      alert("All fields required ❌");
      return;
    }

    try {
      const res = await signupUser({ name, email, password });

      console.log("Signup Response:", res);

     if (res?.message) {
  alert("Check OTP in backend console 🔥");
  navigate("/verify-otp");
} else {
  alert(res?.error || "Signup failed ❌");
}

    } catch (err) {
      console.error(err);
      alert("Server error ❌");
    }
  };

  return (
    <div className="w-[900px] h-[550px] bg-white rounded-2xl shadow-2xl flex overflow-hidden">

      {/* LEFT PANEL */}
      <div className="w-1/2 bg-gradient-to-br from-purple-500 to-indigo-600 text-white flex flex-col justify-center items-center p-10 rounded-r-[120px]">
        <h2 className="text-3xl font-bold mb-4">Hello, Friend!</h2>
        <p className="text-sm text-center mb-6">
          Register to continue
        </p>

        <Link to="/">
          <button className="border border-white px-6 py-2 rounded-full hover:bg-white hover:text-purple-700 transition">
            SIGN IN
          </button>
        </Link>
      </div>

      {/* RIGHT PANEL */}
      <div className="w-1/2 flex flex-col justify-center px-10">

        <h2 className="text-2xl font-bold mb-4 text-center">Create Account</h2>

        {/* SOCIAL LOGIN */}
        <div className="flex justify-center gap-3 mb-4">

          <button
            onClick={() => window.location.href = "http://localhost:8000/api/auth/google"}
            className="border w-10 h-10 rounded-full flex items-center justify-center hover:bg-gray-100"
          >
            <FcGoogle size={20} />
          </button>

          <button
            onClick={() => window.location.href = "http://localhost:8000/api/auth/facebook"}
            className="border w-10 h-10 rounded-full flex items-center justify-center hover:bg-gray-100"
          >
            <FaFacebookF />
          </button>

          <button
            onClick={() => window.location.href = "http://localhost:8000/api/auth/linkedin"}
            className="border w-10 h-10 rounded-full flex items-center justify-center hover:bg-gray-100"
          >
            <FaLinkedinIn />
          </button>

        </div>

        <p className="text-center text-gray-500 text-sm mb-4">
          or use your email for registration
        </p>

        {/* FORM */}
        <form onSubmit={handleSignup} className="space-y-3">

          <input
            type="text"
            placeholder="Name"
            className="w-full p-3 bg-gray-100 rounded-lg outline-none"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 bg-gray-100 rounded-lg outline-none"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 bg-gray-100 rounded-lg outline-none"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          <button
            type="submit"
            className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition"
          >
            SIGN UP
          </button>

        </form>
      </div>
    </div>
  );
}