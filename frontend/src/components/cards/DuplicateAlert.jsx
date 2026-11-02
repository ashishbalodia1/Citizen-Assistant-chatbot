import React from "react";
import { getCategoryBadgeColor } from "../../utils/formatResponse";

export default function DuplicateAlert({ data, onTrackExisting, onProceedAnyway }) {
  if (!data) return null;

  const topMatch = data.top_match || (data.candidates && data.candidates[0]);

  return (
    <div className="bg-[#fff9e6] border-3 border-black rounded-2xl p-4 shadow-[4px_4px_0px_#000] my-2 max-w-md w-full">
      <div className="flex items-center space-x-2 border-b-2 border-black pb-2 mb-2.5">
        <div className="w-8 h-8 rounded-lg bg-[#e52521] border-2 border-black flex items-center justify-center font-bold text-white shadow-[2px_2px_0px_#000]">
          🐢
        </div>
        <div>
          <h4 className="text-xs font-bold mario-font text-slate-900">
            DUPLICATE DETECTED!
          </h4>
          <span className="text-[10px] text-amber-800 font-bold">
            A similar report already exists nearby.
          </span>
        </div>
      </div>

      {topMatch && (
        <div className="bg-white p-3 rounded-xl border-2 border-black text-xs mb-3 space-y-1.5 shadow-[2px_2px_0px_#000]">
          <div className="flex items-center justify-between">
            <span
              className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getCategoryBadgeColor(
                topMatch.category
              )}`}
            >
              {topMatch.category}
            </span>
            {topMatch.distance_meters !== null && (
              <span className="text-amber-800 font-bold text-[11px]">
                📍 ~{topMatch.distance_meters}m away
              </span>
            )}
          </div>

          <p className="text-slate-800 font-semibold">{topMatch.description}</p>

          <div className="flex items-center justify-between text-[11px] font-bold text-slate-600 pt-1 border-t border-slate-200">
            <span>Status: <strong className="text-slate-900">{topMatch.status}</strong></span>
            {topMatch.mission_id && (
              <span className="text-[#00a800] mario-font text-[10px]">
                MISSION #{topMatch.mission_id}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Decision Buttons */}
      <div className="flex items-center gap-2 pt-1">
        {topMatch?.mission_id ? (
          <button
            onClick={() => onTrackExisting && onTrackExisting(topMatch.mission_id)}
            className="flex-1 bg-[#00a800] hover:bg-[#009000] text-white text-[10px] mario-font py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer"
          >
            TRACK MISSION #{topMatch.mission_id}
          </button>
        ) : (
          <button
            onClick={() => onTrackExisting && onTrackExisting(topMatch?.complaint_id)}
            className="flex-1 bg-[#00a800] hover:bg-[#009000] text-white text-[10px] mario-font py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer"
          >
            VIEW COMPLAINT #{topMatch?.complaint_id}
          </button>
        )}

        <button
          onClick={() => onProceedAnyway && onProceedAnyway()}
          className="bg-slate-200 hover:bg-slate-300 text-slate-900 text-xs font-bold py-2 px-3 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer"
        >
          Proceed
        </button>
      </div>
    </div>
  );
}
