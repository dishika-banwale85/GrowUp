import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";
import { GoogleLogin } from "@react-oauth/google";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    if (!username.trim() || !password.trim()) {
      setError("Please enter both username and password.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    try {
      await api.post("/api/signup/", { username, password });
      navigate("/login");
    } catch (err) {
  console.log("SIGNUP ERROR:", err.response?.data);
  setError("Signup failed. Try a different username.");
}
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      // Google signup = same as Google login, account auto-created if new
      const res = await api.post("/api/auth/google/", {
        credential: credentialResponse.credential,
      });
      localStorage.setItem("access", res.data.access);
      localStorage.setItem("refresh", res.data.refresh);
      navigate("/dashboard");
    } catch (err) {
      setError("Google signup failed. Please try again.");
    }
  };

  return (
<div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center">    
<div className="bg-white p-10 rounded-3xl shadow-2xl w-full max-w-lg mx-4">
            <h2 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 mb-6 text-center">
  Create Account ✨
</h2>
<p className="text-center text-gray-500 mb-6">
  Join and start growing your social presence
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
          onClick={handleSignup}
className="w-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 text-white py-4 rounded-2xl font-semibold shadow-lg hover:shadow-xl hover:scale-[1.02] transition duration-300"        >
          Sign Up
        </button>

<div className="flex items-center my-6 gap-3">
  <div className="flex-1 h-px bg-gray-200"></div>
  <span className="text-xs text-gray-400">or</span>
  <div className="flex-1 h-px bg-gray-200"></div>
</div>

        <div className="flex justify-center">
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => setError("Google signup failed. Please try again.")}
            text="signup_with"
            shape="rectangular"
            width="100%"
          />
        </div>

        <p className="text-center text-sm mt-4 text-gray-500">
          Already have an account?{" "}
          <span
            onClick={() => navigate("/login")}
className="text-indigo-600 cursor-pointer font-semibold hover:text-pink-500 transition"          >
            Login
          </span>
        </p>
      </div>
    </div>
  );
}