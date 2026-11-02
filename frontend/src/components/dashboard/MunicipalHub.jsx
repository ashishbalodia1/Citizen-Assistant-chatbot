import React, { useState, useEffect } from "react";
import axios from "axios";
import { CheckCircle2, XCircle, RefreshCw } from "lucide-react";
import { getCategoryBadgeColor } from "../../utils/formatResponse";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

export default function MunicipalHub({ onClose }) {
  const [complaints, setComplaints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("PENDING_VERIFICATION");
  const [actionLoading, setActionLoading] = useState(null);
  const [message, setMessage] = useState(null);

  const token = localStorage.getItem("access_token");

  const fetchComplaints = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/complaints?status=${filter}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.data.success) {
        setComplaints(res.data.complaints || []);
      }
    } catch (err) {
      console.error("Failed to load complaints for verification:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchComplaints();
  }, [filter]);

  const handleVerify = async (complaintId, action) => {
    try {
      setActionLoading(complaintId);
      setMessage(null);
      const res = await axios.post(
        `${API_BASE}/complaints/${complaintId}/verify`,
        { action, notes: "Verified by Officer Gupta (Ward Inspection)" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (res.data.success) {
        setMessage(res.data.message);
        fetchComplaints();
      }
    } catch (err) {
      console.error("Verification failed:", err);
      setMessage("Action failed. Ensure you are logged in as Municipal Officer.");
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="flex flex-col h-[82vh] max-w-4xl mx-auto w-full bg-[#f8fafc] border-4 border-black rounded-2xl shadow-[6px_6px_0px_#000] overflow-hidden">
      {/* Header */}
      <div className="bg-[#ffffff] border-b-4 border-black px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-11 h-11 rounded-xl bg-[#00a800] border-3 border-black flex items-center justify-center font-bold text-xl text-white shadow-[3px_3px_0px_#000]">
            🏰
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h2 className="text-xs sm:text-sm font-black mario-font text-slate-900">
                OFFICER CASTLE
              </h2>
              <span className="bg-[#ffd700] text-black text-[9px] font-bold px-2 py-0.5 rounded border-2 border-black mario-font shadow-[1px_1px_0px_#000]">
                PORTAL
              </span>
            </div>
            <p className="text-[11px] font-bold text-slate-600 mt-0.5">
              Human-in-the-Loop Municipal Verification & Squad Dispatch
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={fetchComplaints}
            className="p-1.5 bg-slate-100 hover:bg-slate-200 border-2 border-black rounded-lg transition shadow-[2px_2px_0px_#000] cursor-pointer"
            title="Refresh List"
          >
            <RefreshCw className="w-4 h-4 text-slate-700" />
          </button>
          <button
            onClick={onClose}
            className="bg-[#e52521] hover:bg-[#c91d1a] text-white text-[10px] mario-font px-3 py-2 rounded-lg border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer"
          >
            🍄 CITIZEN CHAT
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex border-b-2 border-black bg-white px-3 pt-2 gap-1.5 text-xs overflow-x-auto">
        {[
          { key: "PENDING_VERIFICATION", label: "PENDING REVIEW" },
          { key: "APPROVED", label: "APPROVED" },
          { key: "IN_PROGRESS", label: "IN PROGRESS" },
          { key: "RESOLVED", label: "RESOLVED" }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`pb-2 px-3 text-[10px] mario-font transition border-b-4 cursor-pointer whitespace-nowrap ${
              filter === tab.key
                ? "border-[#e52521] text-[#e52521] font-bold"
                : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Alert message if any */}
      {message && (
        <div className="mx-4 mt-3 p-2.5 bg-[#e6f9ed] border-2 border-black text-emerald-900 text-xs font-bold rounded-xl shadow-[2px_2px_0px_#000] flex items-center justify-between">
          <span>{message}</span>
          <button onClick={() => setMessage(null)} className="font-bold text-slate-600 hover:text-black">✕</button>
        </div>
      )}

      {/* Complaints List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-[#eef2f6]">
        {loading ? (
          <div className="text-center py-12 text-slate-500 text-xs mario-font">Loading records...</div>
        ) : complaints.length === 0 ? (
          <div className="text-center py-12 text-slate-500 text-xs mario-font">
            No complaints under filter: {filter}
          </div>
        ) : (
          complaints.map((comp) => (
            <div
              key={comp.id}
              className="bg-white border-3 border-black rounded-2xl p-4 shadow-[3px_3px_0px_#000] flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center space-x-2">
                  <span className="mario-font text-xs font-bold text-slate-900">#{comp.id}</span>
                  <span
                    className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getCategoryBadgeColor(
                      comp.category
                    )}`}
                  >
                    {comp.category}
                  </span>
                  <span className="text-[9px] mario-font bg-slate-100 text-slate-700 border border-black px-2 py-0.5 rounded">
                    {comp.status}
                  </span>
                </div>

                <p className="text-xs text-slate-900 font-semibold leading-relaxed">
                  {comp.description}
                </p>

                <div className="flex items-center space-x-3 text-[11px] text-slate-600 font-bold pt-1">
                  <span>📍 {comp.address || "Sector 4, Ward 7"}</span>
                  <span>📅 {comp.created_at ? comp.created_at.substring(0, 10) : "Recent"}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2 flex-shrink-0">
                {comp.status === "PENDING_VERIFICATION" && (
                  <>
                    <button
                      onClick={() => handleVerify(comp.id, "APPROVE")}
                      disabled={actionLoading === comp.id}
                      className="flex items-center gap-1 bg-[#00a800] hover:bg-[#009000] text-white text-[10px] mario-font py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer disabled:opacity-50"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      APPROVE & SQUAD
                    </button>
                    <button
                      onClick={() => handleVerify(comp.id, "REJECT")}
                      disabled={actionLoading === comp.id}
                      className="flex items-center gap-1 bg-slate-200 hover:bg-slate-300 text-rose-700 text-xs font-bold py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer disabled:opacity-50"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      Reject
                    </button>
                  </>
                )}

                {(comp.status === "APPROVED" || comp.status === "IN_PROGRESS") && (
                  <button
                    onClick={() => handleVerify(comp.id, "RESOLVE")}
                    disabled={actionLoading === comp.id}
                    className="flex items-center gap-1 bg-[#ffd700] hover:bg-[#ffc800] text-black text-[10px] mario-font py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer disabled:opacity-50"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    MARK RESOLVED
                  </button>
                )}

                {comp.status === "RESOLVED" && (
                  <span className="text-[#00a800] text-[10px] mario-font font-bold flex items-center gap-1 bg-[#e6f9ed] border-2 border-black px-3 py-1.5 rounded-xl shadow-[1px_1px_0px_#000]">
                    <CheckCircle2 className="w-4 h-4" /> VERIFIED & CLOSED
                  </span>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
