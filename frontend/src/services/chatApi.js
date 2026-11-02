import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

const API = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const sendMessage = async (message, sessionId = null, coordinates = null) => {
  const response = await API.post("/chat", {
    message,
    session_id: sessionId,
    coordinates,
  });
  return response.data;
};

export const getConversationHistory = async (sessionId) => {
  const response = await API.get(`/conversations/${sessionId}`);
  return response.data;
};

export const fetchMission = async (missionId) => {
  const response = await API.get(`/missions/${missionId}`);
  return response.data;
};

export const fetchRewards = async () => {
  const response = await API.get("/rewards");
  return response.data;
};

export const fetchCoupons = async () => {
  const response = await API.get("/coupons");
  return response.data;
};

export const redeemCoupon = async (couponId) => {
  const response = await API.post("/coupons/redeem", { coupon_id: couponId });
  return response.data;
};

export const confirmComplaint = async (complaintData) => {
  const response = await API.post("/complaints", complaintData);
  return response.data;
};

export const loginDemoUser = async (userId = 1) => {
  const response = await API.post("/auth/token", { user_id: userId });
  if (response.data.access_token) {
    localStorage.setItem("access_token", response.data.access_token);
  }
  return response.data;
};

export default API;

