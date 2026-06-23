import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";

export default function Dashboard() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access");
    if (!token) {
      navigate("/login");
      return;
    }

    // Fetch profile from Django
    api.get("/api/profile/")
      .then((res) => {
        setProfile(res.data);
        setLoading(false);
      })
      .catch(() => {
        // Token invalid or expired — log out
        localStorage.clear();
        navigate("/login");
      });
  }, [navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-100">
        <p className="text-indigo-600 font-semibold text-lg animate-pulse">Loading...</p>
      </div>
    );
  }

  const initials = profile
    ? `${profile.first_name?.[0] || ''}${profile.last_name?.[0] || ''}`.toUpperCase() || profile.username?.[0]?.toUpperCase()
    : '?';

  return (
    <div className="min-h-screen bg-slate-100 flex">

      {/* Sidebar */}
      <div className="w-72 bg-gradient-to-b from-indigo-700 to-purple-700 text-white flex flex-col shadow-xl">

        {/* Profile Preview */}
        <div className="p-6 border-b border-indigo-500">
          {/* Avatar */}
          <div className="flex justify-center mb-3">
            {profile?.profile_picture ? (
              <img
                src={profile.profile_picture}
                alt="Profile"
                className="w-16 h-16 rounded-full border-2 border-white object-cover"
              />
            ) : (
              <div className="w-16 h-16 rounded-full bg-white text-indigo-700 flex items-center justify-center text-2xl font-bold border-2 border-indigo-300">
                {initials}
              </div>
            )}
          </div>

          {/* Name & username */}
          <div className="text-center">
            <p className="font-bold text-lg leading-tight">
              {profile?.first_name && profile?.last_name
                ? `${profile.first_name} ${profile.last_name}`
                : profile?.username}
            </p>
            <p className="text-indigo-200 text-sm">@{profile?.username}</p>
            <p className="text-indigo-300 text-xs mt-1 truncate">{profile?.email}</p>
          </div>

          {/* New / Member badge */}
          <div className="flex justify-center mt-3">
            {profile?.is_new ? (
              <span className="bg-yellow-400 text-yellow-900 text-xs font-bold px-3 py-1 rounded-full">
                🌟 New Member
              </span>
            ) : (
              <span className="bg-indigo-500 text-white text-xs px-3 py-1 rounded-full">
                ✅ Member since {profile?.joined_date}
              </span>
            )}
          </div>

          {/* Quick stats */}
          <div className="flex justify-around mt-4 text-center">
            <div>
              <p className="text-xl font-bold">{profile?.total_posts}</p>
              <p className="text-indigo-200 text-xs">Posts</p>
            </div>
            <div className="border-l border-indigo-500" />
            <div>
              <p className="text-xl font-bold">{profile?.scheduled_posts}</p>
              <p className="text-indigo-200 text-xs">Scheduled</p>
            </div>
            <div className="border-l border-indigo-500" />
            <div>
              <p className="text-xl font-bold">{profile?.connected_providers?.length}</p>
              <p className="text-indigo-200 text-xs">Connected</p>
            </div>
          </div>

          {/* Connected platforms */}
          {profile?.connected_providers?.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-1 justify-center">
              {profile.connected_providers.map((p) => (
                <span key={p} className="bg-indigo-600 text-xs px-2 py-0.5 rounded-full capitalize">
                  {p}
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Navigation */}
        <nav className="p-6 flex-1 space-y-4">
          <p className="text-indigo-300 text-xs uppercase tracking-widest font-semibold">Menu</p>
          <li
            onClick={() => navigate("/dashboard")}
            className="list-none cursor-pointer font-semibold text-yellow-300"
          >
            📊 Dashboard
          </li>
          <li
            onClick={() => navigate("/create")}
            className="list-none cursor-pointer hover:text-gray-200"
          >
            ✏️ Create Post
          </li>
          <li className="list-none cursor-pointer hover:text-gray-200">
            🕐 Scheduled Posts
          </li>
          <li className="list-none cursor-pointer hover:text-gray-200">
            📈 Analytics
          </li>
        </nav>

        {/* Logout */}
        <div className="p-6 border-t border-indigo-500">
          <button
            onClick={() => { localStorage.clear(); navigate("/login"); }}
            className="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold transition text-sm"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-slate-800">
            {profile?.is_new
              ? `Welcome to GrowUp, ${profile?.first_name || profile?.username}! 🎉`
              : `Welcome back, ${profile?.first_name || profile?.username}! 👋`}
          </h2>
          <p className="text-slate-500 mt-1">
            {profile?.is_new
              ? "Your account is all set. Start by creating your first post!"
              : `You've been with us since ${profile?.joined_date}.`}
          </p>
        </div>

        {/* Stats cards */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow text-center">
            <p className="text-gray-500 text-sm mb-1">Total Posts</p>
            <p className="text-4xl font-bold text-indigo-600">{profile?.total_posts}</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow text-center">
            <p className="text-gray-500 text-sm mb-1">Scheduled</p>
            <p className="text-4xl font-bold text-purple-600">{profile?.scheduled_posts}</p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow text-center">
            <p className="text-gray-500 text-sm mb-1">Connected Platforms</p>
            <p className="text-4xl font-bold text-green-600">{profile?.connected_providers?.length}</p>
          </div>
        </div>

        {/* Quick actions */}
        <div className="bg-white p-6 rounded-xl shadow">
          <h3 className="text-xl font-bold mb-4 text-slate-800">Quick Actions</h3>
          <div className="flex gap-4">
            <button
              onClick={() => navigate("/create")}
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
            >
              + Create New Post
            </button>
            <button
              className="bg-slate-100 text-slate-700 px-6 py-3 rounded-lg font-semibold hover:bg-slate-200 transition"
            >
              🔗 Connect Platform
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}