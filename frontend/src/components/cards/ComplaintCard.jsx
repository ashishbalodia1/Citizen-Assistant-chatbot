import React from "react";
import { getCategoryBadgeColor } from "../../utils/formatResponse";

export default function ComplaintCard({ data, onConfirm, onCancel, loading }) {
  if (!data) return null;

  const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://127.0.0.1:5000";
  const imageSrc = data.image_path ? `${backendUrl}/${data.image_path}` : null;

  return (
    <div className="bg-[#ffffff] border-3 border-black rounded-2xl p-4 shadow-[4px_4px_0px_#000] my-2 max-w-md w-full">
      {/* Title */}
      <div className="flex items-center justify-between border-b-2 border-black pb-2.5 mb-2.5">
        <div className="flex items-center space-x-2">
          {/* Question Mark Box */}
          <div className="w-8 h-8 rounded-lg bg-[#ffd700] border-2 border-black flex items-center justify-center font-bold text-sm shadow-[2px_2px_0px_#000] mario-font text-black">
            ?
          </div>
          <div>
            <h4 className="text-xs font-bold mario-font text-slate-900">
              DRAFT REPORT
            </h4>
            <span className="text-[10px] text-amber-700 font-bold block">
              ★ Citizen Confirmation Required
            </span>
          </div>
        </div>
        <span
          className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getCategoryBadgeColor(
            data.category
          )}`}
        >
          {data.category || "Civic Issue"}
        </span>
      </div>

      {/* Description */}
      <div className="bg-[#fffdf0] p-3 rounded-xl border-2 border-black mb-3 shadow-[2px_2px_0px_#000]">
        <span className="text-[9px] mario-font text-[#e52521] block mb-1">
          GRIEVANCE SUMMARY:
        </span>
        <p className="text-xs text-slate-800 font-semibold leading-relaxed">{data.description}</p>
      </div>

      {/* Location info */}
      <div className="flex items-center space-x-1.5 text-xs text-slate-700 mb-3 bg-slate-100 p-2 rounded-xl border border-slate-300 font-bold">
        <span>📍</span>
        <span className="truncate">{data.address || "GPS Location Coordinates Attached"}</span>
      </div>

      {/* Image Preview if available */}
      {imageSrc && (
        <div className="mb-3 rounded-xl overflow-hidden border-2 border-black max-h-36 relative">
          <img
            src={imageSrc}
            alt="Complaint Evidence"
            className="w-full h-36 object-cover"
            onError={(e) => {
              e.target.style.display = "none";
            }}
          />
          <div className="absolute bottom-1 right-1 bg-black text-[9px] mario-font text-white px-2 py-0.5 rounded">
            PHOTO EVIDENCE
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center gap-2 pt-2 border-t-2 border-slate-200">
        <button
          onClick={() => onConfirm && onConfirm(data)}
          disabled={loading}
          className="flex-1 flex items-center justify-center gap-1.5 bg-[#00a800] hover:bg-[#009000] text-white text-xs mario-font py-2.5 px-3 rounded-xl border-2 border-black shadow-[3px_3px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition disabled:opacity-50 cursor-pointer"
        >
          <span>CONFIRM (+15 🪙)</span>
        </button>
        <button
          onClick={() => onCancel && onCancel()}
          disabled={loading}
          className="bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-bold py-2.5 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition disabled:opacity-50 cursor-pointer"
        >
          CANCEL
        </button>
      </div>
    </div>
  );
}
