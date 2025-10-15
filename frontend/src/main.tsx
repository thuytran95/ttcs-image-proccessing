import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";

const container = document.getElementById("root");
if (!container) throw new Error("Không tìm thấy phần tử #root trong DOM");

createRoot(container).render(
  <StrictMode>
    <App />
  </StrictMode>
);
