import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

export const uploadVoice = async (audioBlob, sessionId = null) => {
  const formData = new FormData();
  formData.append("audio", audioBlob, "voice_report.webm");
  if (sessionId) {
    formData.append("session_id", sessionId);
  }

  const token = localStorage.getItem("access_token");
  const headers = { "Content-Type": "multipart/form-data" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await axios.post(`${API_BASE}/upload/voice`, formData, {
    headers,
  });
  return response.data;
};

export const speakMessage = (text, language = "hi-IN") => {
  if (!("speechSynthesis" in window)) {
    console.warn("Speech synthesis not supported in this browser.");
    return;
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel();

  // Strip markdown formatting for cleaner speech
  const cleanText = text
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/\*(.*?)\*/g, "$1")
    .replace(/#+/g, "")
    .replace(/`{1,3}.*?`{1,3}/gs, "");

  const utterance = new SpeechSynthesisUtterance(cleanText);
  utterance.lang = language;
  utterance.rate = 1.0;
  utterance.pitch = 1.0;

  // Try to find a natural Hindi or Indian English voice if available
  const voices = window.speechSynthesis.getVoices();
  const indianVoice = voices.find(
    (v) => v.lang.includes("hi") || v.lang.includes("en-IN")
  );
  if (indianVoice) {
    utterance.voice = indianVoice;
  }

  window.speechSynthesis.speak(utterance);
};

