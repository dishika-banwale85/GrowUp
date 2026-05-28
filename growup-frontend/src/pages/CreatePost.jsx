import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";

export default function CreatePost() {
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState(null);
  const [scheduleTime, setScheduleTime] = useState("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("caption", caption);
    formData.append("file", file);
    formData.append("scheduled_time", scheduleTime);
    try {
      await api.post("/api/create-post/", formData);
      setSuccess("Post scheduled successfully 🚀");
      setError("");
    } catch (err) {
      setError("Failed to create post. Please login again.");
      setSuccess("");
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-indigo-600 text-white p-6">
        <h1 className="text-2xl font-bold mb-8">GrowUp</h1>
        <ul className="space-y-4">
          <li onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-gray-200">Dashboard</li>
          <li className="cursor-pointer font-semibold">Create Post</li>
          <li className="cursor-pointer hover:text-gray-200">Scheduled</li>
          <li onClick={() => { localStorage.clear(); navigate("/login"); }} className="cursor-pointer hover:text-red-300 mt-8">Logout</li>
        </ul>
      </div>
      {/* Main Content */}
      <div className="flex-1 p-8">
        <div className="flex items-center gap-4 mb-6">
          <button onClick={() => navigate("/dashboard")} className="text-indigo-600 font-semibold hover:underline">← Back to Dashboard</button>
          <h2 className="text-3xl font-bold">Create Post</h2>
        </div>
        {success && <p className="text-green-600 mb-4 font-semibold">{success}</p>}
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <div className="bg-white p-6 rounded-lg shadow max-w-xl">
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            className="mb-4 w-full"
          />
          <textarea
            placeholder="Write your caption..."
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            className="w-full border p-3 rounded mb-4 outline-none focus:border-indigo-500"
            rows={4}
          />
          <input
            type="datetime-local"
            value={scheduleTime}
            onChange={(e) => setScheduleTime(e.target.value)}
            className="w-full border p-2 rounded mb-4 outline-none focus:border-indigo-500"
          />
          <button
            onClick={handleSubmit}
            className="w-full bg-indigo-600 text-white px-4 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Schedule Post 🚀
          </button>
        </div>
      </div>
    </div>
  );
}