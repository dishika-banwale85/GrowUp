import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { FaInstagram, FaFacebook, FaLinkedin, FaYoutube } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import { FiUploadCloud, FiCalendar } from "react-icons/fi";
import api from "./api";

export default function CreatePost() {
  const navigate = useNavigate();
  const [caption, setCaption] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [scheduleTime, setScheduleTime] = useState("");
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [connectedAccounts, setConnectedAccounts] = useState({});
  const [showConnectModal, setShowConnectModal] = useState(null); // platform name

  const [platforms, setPlatforms] = useState({
    instagram: false,
    facebook: false,
    x: false,
    linkedin: false,
    youtube: false,
  });

  // Fetch connected accounts on mount
  useEffect(() => {
    api.get("/api/connected-accounts/")
      .then(res => setConnectedAccounts(res.data))
      .catch(() => {});
  }, []);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  };

  const handlePlatformClick = (name) => {
    // If platform supports connection (instagram/facebook)
    if (name === 'instagram' || name === 'facebook') {
      if (!connectedAccounts[name]) {
        // Not connected — show connect modal
        setShowConnectModal(name);
        return;
      }
    }
    // Toggle selection
    setPlatforms(prev => ({ ...prev, [name]: !prev[name] }));
  };

  const handleConnect = (platform) => {
    // Redirect to Django OAuth flow
    if (platform === 'instagram') {
      window.location.href = `${import.meta.env.VITE_API_URL}/auth/instagram/login/`;
    } else if (platform === 'facebook') {
      window.location.href = `${import.meta.env.VITE_API_URL}/account/facebook/login/`;
    }
    setShowConnectModal(null);
  };

  const handleSubmit = async () => {
    setError("");

    if (!file) { setError("Please upload a photo or video."); return; }
    if (!caption.trim()) { setError("Please enter a caption."); return; }
    if (!scheduleTime) { setError("Please choose a schedule time."); return; }
    if (new Date(scheduleTime) <= new Date()) { setError("Schedule time must be in the future."); return; }

    const selectedPlatforms = Object.keys(platforms).filter(k => platforms[k]);
    if (selectedPlatforms.length === 0) { setError("Please select at least one platform."); return; }

    // Check all selected platforms are connected
    const notConnected = selectedPlatforms.filter(p =>
      (p === 'instagram' || p === 'facebook') && !connectedAccounts[p]
    );
    if (notConnected.length > 0) {
      setError(`Please connect first: ${notConnected.join(', ')}`);
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("caption", caption);
      formData.append("file", file);
      formData.append("scheduled_time", scheduleTime);
      formData.append("platforms", JSON.stringify(selectedPlatforms));

      const res = await api.post("/api/create-post/", formData);

      if (res.data.errors && res.data.errors.length > 0) {
        setError(`Some platforms failed: ${res.data.errors.join(', ')}`);
      }
      if (res.data.success && res.data.success.length > 0) {
        setShowSuccessModal(true);
        setCaption(""); setFile(null); setPreview(""); setScheduleTime("");
        setPlatforms({ instagram: false, facebook: false, x: false, linkedin: false, youtube: false });
      }
    } catch (err) {
      setError("Failed to create post. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const platformConfig = {
    instagram: { icon: <FaInstagram size={28} color="#E1306C" />, label: "Instagram", supported: true },
    facebook: { icon: <FaFacebook size={28} color="#1877F2" />, label: "Facebook", supported: true },
    x: { icon: <FaXTwitter size={28} />, label: "X", supported: false },
    linkedin: { icon: <FaLinkedin size={28} color="#0A66C2" />, label: "LinkedIn", supported: false },
    youtube: { icon: <FaYoutube size={28} color="#FF0000" />, label: "YouTube", supported: false },
  };

  return (
    <div className="min-h-screen bg-slate-100 flex">

      {/* Sidebar */}
      <div className="w-72 bg-gradient-to-b from-indigo-700 to-purple-700 text-white p-6 shadow-xl">
        <h1 className="text-3xl font-bold mb-10">GrowUp 🚀</h1>
        <ul className="space-y-5">
          <li onClick={() => navigate("/dashboard")} className="cursor-pointer hover:text-gray-200">📊 Dashboard</li>
          <li className="font-semibold text-yellow-300">✏️ Create Post</li>
          <li className="cursor-pointer hover:text-gray-200">🕐 Scheduled Posts</li>
          <li className="cursor-pointer hover:text-gray-200">📈 Analytics</li>
        </ul>
        <button
          onClick={() => { localStorage.clear(); navigate("/login"); }}
          className="mt-10 w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold transition text-sm"
        >Logout</button>
      </div>

      {/* Main */}
      <div className="flex-1 p-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-4xl font-bold text-gray-800">Create Social Post</h2>
            <p className="text-gray-500 mt-1">Upload media, write a caption and publish.</p>
          </div>
          <button onClick={() => navigate("/dashboard")} className="text-indigo-600 font-semibold">← Dashboard</button>
        </div>

        {error && <div className="bg-red-100 text-red-600 p-3 rounded-xl mb-4">{error}</div>}

        <div className="grid lg:grid-cols-2 gap-8">

          {/* Media Upload */}
          <div className="bg-white rounded-3xl shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Media Preview</h3>
            <label className="border-2 border-dashed border-indigo-300 rounded-2xl flex flex-col items-center justify-center h-80 cursor-pointer hover:bg-indigo-50 transition">
              <FiUploadCloud size={50} className="text-indigo-500" />
              <p className="mt-3 font-medium">Upload Photo or Video</p>
              <p className="text-sm text-gray-500">Drag & drop or click here</p>
              <input type="file" accept="image/*,video/*" hidden onChange={handleFileChange} />
            </label>
            {preview && (
              <div className="mt-5">
                {file.type.startsWith("image") ? (
                  <img src={preview} alt="preview" className="rounded-2xl w-full h-80 object-cover" />
                ) : (
                  <video controls className="rounded-2xl w-full h-80">
                    <source src={preview} />
                  </video>
                )}
              </div>
            )}
          </div>

          {/* Post Details */}
          <div className="bg-white rounded-3xl shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4">Post Details</h3>

            {/* Caption */}
            <div className="mb-6">
              <div className="flex justify-between mb-2">
                <label className="font-medium">Caption</label>
                <span className="text-sm text-gray-500">{caption.length}/2200</span>
              </div>
              <textarea
                rows="5"
                value={caption}
                onChange={(e) => setCaption(e.target.value)}
                placeholder="Write an engaging caption..."
                className="w-full border rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            {/* Platforms */}
            <div className="mb-6">
              <label className="font-medium block mb-3">Select Platforms</label>
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(platformConfig).map(([key, config]) => {
                  const isConnected = connectedAccounts[key];
                  const isSelected = platforms[key];
                  const isSupported = config.supported;

                  return (
                    <div
                      key={key}
                      onClick={() => handlePlatformClick(key)}
                      className={`cursor-pointer border rounded-2xl p-4 flex items-center gap-3 transition relative
                        ${isSelected ? "border-indigo-500 bg-indigo-50" : "border-gray-200"}
                        ${!isSupported ? "opacity-50" : ""}
                      `}
                    >
                      {config.icon}
                      <div className="flex-1">
                        <span className="font-medium">{config.label}</span>
                        {isSupported && (
                          <p className="text-xs mt-0.5">
                            {isConnected
                              ? <span className="text-green-600">✅ @{connectedAccounts[key]?.username}</span>
                              : <span className="text-orange-500">Tap to connect</span>
                            }
                          </p>
                        )}
                        {!isSupported && (
                          <p className="text-xs text-gray-400 mt-0.5">Coming soon</p>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Schedule */}
            <div className="mb-8">
              <label className="font-medium block mb-3">Schedule Time</label>
              <div className="relative">
                <FiCalendar className="absolute left-4 top-4 text-gray-500" />
                <input
                  type="datetime-local"
                  value={scheduleTime}
                  onChange={(e) => setScheduleTime(e.target.value)}
                  className="w-full border rounded-xl p-3 pl-12"
                />
              </div>
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                onClick={() => navigate("/dashboard")}
                className="flex-1 bg-gray-200 py-3 rounded-xl font-semibold hover:bg-gray-300"
              >Cancel</button>
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="flex-1 bg-indigo-600 text-white py-3 rounded-xl font-semibold hover:bg-indigo-700 transition disabled:opacity-60"
              >
                {loading ? "Posting..." : "Post 🚀"}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* CONNECT MODAL */}
      {showConnectModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-3xl p-8 w-[400px] text-center shadow-2xl">
            <div className="text-6xl mb-4">
              {showConnectModal === 'instagram' ? '📸' : '📘'}
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-3">
              Connect {showConnectModal === 'instagram' ? 'Instagram' : 'Facebook'}
            </h2>
            <p className="text-gray-500 mb-6">
              {showConnectModal === 'instagram'
                ? 'Connect your Instagram Business account to start posting.'
                : 'Connect your Facebook Page to start posting.'}
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowConnectModal(null)}
                className="flex-1 bg-gray-100 py-3 rounded-xl font-semibold hover:bg-gray-200"
              >Cancel</button>
              <button
                onClick={() => handleConnect(showConnectModal)}
                className="flex-1 bg-indigo-600 text-white py-3 rounded-xl font-semibold hover:bg-indigo-700"
              >Connect Now</button>
            </div>
          </div>
        </div>
      )}

      {/* SUCCESS MODAL */}
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-3xl p-8 w-[420px] text-center shadow-2xl">
            <div className="text-7xl mb-4">🎉</div>
            <h2 className="text-3xl font-bold text-gray-800 mb-3">Post Published!</h2>
            <p className="text-gray-600 mb-6">
              Your content has been successfully published to the selected platforms.
            </p>
            <button
              onClick={() => { setShowSuccessModal(false); navigate("/dashboard"); }}
              className="bg-indigo-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-indigo-700"
            >Awesome!</button>
          </div>
        </div>
      )}
    </div>
  );
}