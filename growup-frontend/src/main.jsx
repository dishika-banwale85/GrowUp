import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { GoogleOAuthProvider } from "@react-oauth/google";

import "./index.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <GoogleOAuthProvider clientId="792664826369-mu65ssejfl51hn72r6frefh01aummvu1.apps.googleusercontent.com">
      <App />
    </GoogleOAuthProvider>
  </StrictMode>
);