import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";
import { GoogleLogin } from "@react-oauth/google";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }
    try {
      const res = await api.post("/api/token/", { username, password });
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid username or password.");
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // Send Google credential to Django to verify and get JWT tokens
      const res = await api.post("/api/auth/google/", {
        credential: credentialResponse.credential,
      });
      // Save JWT tokens exactly like normal login
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      navigate("/dashboard");
    } catch (err) {
  console.log("GOOGLE ERROR:", err.response?.data);
  console.log("GOOGLE STATUS:", err.response?.status);
  setError("Google login failed. Please try again.");
}
  };

  return (
<div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center">  
<div className="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-lg mx-4">
  <h2 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 mb-6 text-center">          Welcome Back ✨
        </h2>
        <p className="text-center text-gray-500 mb-6">
  Login to continue your growth journey
</p>
        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">{error}</p>
        )}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
className="w-full border border-gray-200 p-4 rounded-2xl mb-4 outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition"        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
className="w-full border border-gray-200 p-4 rounded-2xl mb-6 outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition"        />
        <button
          onClick={handleLogin}
className="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white py-4 rounded-2xl font-semibold shadow-lg hover:shadow-xl hover:scale-[1.02] transition duration-300"        >
          Login
        </button>

        <div className="flex items-center my-4">
<hr className="flex-1 border-gray-200" />
<span className="px-3 text-gray-400 text-xs">or</span>          <hr className="flex-1 border-gray-300" />
        </div>

<div className="flex justify-center mt-2">          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => setError("Google login failed. Please try again.")}
            text="continue_with"
            shape="rectangular"
            width="100%"
          />
        </div>

        <p className="text-center text-sm mt-4 text-gray-500">
          Don't have an account?{" "}
          <span
            onClick={() => navigate("/signup")}
className="text-indigo-600 cursor-pointer font-semibold hover:text-pink-500 transition"          >
            Sign Up
          </span>
        </p>
      </div>
    </div>
  );
}