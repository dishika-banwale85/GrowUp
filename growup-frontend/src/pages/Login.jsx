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
    <div className="min-h-screen bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-md">
        <h2 className="text-3xl font-bold text-indigo-600 mb-6 text-center">
          Welcome Back 👋
        </h2>
        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">{error}</p>
        )}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border p-3 rounded-lg mb-4 outline-none focus:border-indigo-500"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border p-3 rounded-lg mb-6 outline-none focus:border-indigo-500"
        />
        <button
          onClick={handleLogin}
          className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
        >
          Login
        </button>

        <div className="flex items-center my-4">
          <hr className="flex-1 border-gray-300" />
          <span className="px-3 text-gray-400 text-sm">or</span>
          <hr className="flex-1 border-gray-300" />
        </div>

        <div className="flex justify-center">
          <GoogleLogin
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
            className="text-indigo-600 cursor-pointer font-semibold"
          >
            Sign Up
          </span>
        </p>
      </div>
    </div>
  );
}