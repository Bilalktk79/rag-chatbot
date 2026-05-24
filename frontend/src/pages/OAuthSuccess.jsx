import { useEffect } from "react";

export default function OAuthSuccess() {

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);

    const token = params.get("token");  // 🔥 FIX

    console.log("TOKEN:", token);

    if (token) {
      localStorage.setItem("token", token);

      // 🔥 IMPORTANT FIX
      window.location.href = "/home";
    } else {
      window.location.href = "/";
    }

  }, []);

  return <h2>Logging you in...</h2>;
}