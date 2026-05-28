import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Dashboard() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
    }
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-indigo-600 text-white p-6 flex flex-col">
        <h1 className="text-2xl font-bold mb-8">GrowUp</h1>
        <ul className="space-y-4 flex-1">
          <li className="cursor-pointer font-semibold">Dashboard</li>
          <li onClick={() => navigate("/create")} className="cursor-pointer hover:text-gray-200">Create Post</li>
          <li className="cursor-pointer hover:text-gray-200">Scheduled</li>
          <li className="cursor-pointer hover:text-gray-200">Settings</li>
        </ul>
        <button
          onClick={() => { localStorage.clear(); navigate("/login"); }}
          className="mt-auto bg-white text-indigo-600 py-2 rounded-lg font-semibold hover:bg-gray-100"
        >
          Logout
        </button>
      </div>
      {/* Main Content */}
      <div className="flex-1 p-8">
        <h2 className="text-3xl font-bold mb-6">Dashboard 🚀</h2>
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow text-center">
            <p className="text-gray-500 text-sm">Total Posts</p>
            <p className="text-4xl font-bold text-indigo-600">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow text-center">
            <p className="text-gray-500 text-sm">Scheduled</p>
            <p className="text-4xl font-bold text-indigo-600">0</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow text-center">
            <p className="text-gray-500 text-sm">Connected Platforms</p>
            <p className="text-4xl font-bold text-indigo-600">0</p>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Quick Actions</h3>
          <button
            onClick={() => navigate("/create")}
            className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            + Create New Post
          </button>
        </div>
      </div>
    </div>
  );
}