import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-600 to-purple-600 text-white">

      <nav className="flex justify-between p-6">
        <h1 className="text-2xl font-bold">GrowUp</h1>
        <button 
        onClick={() => navigate("/login")}
          className="bg-white text-indigo-600 px-4 py-2 rounded-lg"
        >
          Login
        </button>
      </nav>

      <div className="flex flex-col items-center justify-center text-center mt-20 px-4">
        <h1 className="text-5xl font-bold mb-6">
          Manage All Your Social Media in One Place 🚀
        </h1>

        <p className="text-lg mb-8 max-w-xl">
          Upload once, schedule anytime, and post everywhere without wasting time.
        </p>

        <button 

          onClick={() => navigate("/login")}
          className="bg-white text-indigo-600 px-6 py-3 rounded-lg font-semibold"
        >
          Get Started
        </button>
      </div>

    </div>
  );
}