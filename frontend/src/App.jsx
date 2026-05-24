import { Routes, Route } from "react-router-dom";

// Pages
import Login from "./pages/Auth/Login";
import Signup from "./pages/Auth/Signup";
import Chat from "./pages/Chat/Chat";
import Settings from "./pages/Settings/Settings";
import Home from "./pages/Home";
import OAuthSuccess from "./pages/OAuthSuccess";
import VerifyOTP from "./pages/VerifyOTP";
// Layouts
import MainLayout from "./layout/MainLayout";
import AuthLayout from "./layout/AuthLayout";

function App() {
  return (
    <Routes>

      {/* 🔐 Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Route>

      {/* 🌐 Main App Routes */}
      <Route element={<MainLayout />}>
        <Route path="/home" element={<Home />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      {/* 🔥 ADD THIS HERE (IMPORTANT) */}
      <Route path="/oauth-success" element={<OAuthSuccess />} />
       <Route path="/verify-otp" element={<VerifyOTP />} />
    </Routes>
  );
}

export default App;