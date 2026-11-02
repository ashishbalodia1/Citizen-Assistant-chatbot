import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

export const uploadImage = async (file, sessionId = null) => {
  const formData = new FormData();
  formData.append("image", file);
  if (sessionId) {
    formData.append("session_id", sessionId);
  }

  const token = localStorage.getItem("access_token");
  const headers = { "Content-Type": "multipart/form-data" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await axios.post(`${API_BASE}/upload/image`, formData, {
    headers,
  });
  return response.data;
};

