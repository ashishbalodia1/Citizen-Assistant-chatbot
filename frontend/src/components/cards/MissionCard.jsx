import React, { useState, useEffect } from "react";
import { formatRelativeTime, getCategoryBadgeColor } from "../../utils/formatResponse";

export default function MissionCard({ data }) {
  if (!data) return null;

  const [remainingSecs, setRemainingSecs] = useState(
    data.remaining_seconds || 0
  );

  useEffect(() => {
    if (remainingSecs <= 0) return;
    const interval = setInterval(() => {
      setRemainingSecs((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, [remainingSecs]);

  return (
    <div className="bg-[#ffffff] border-3 border-black rounded-2xl p-4 shadow-[4px_4px_0px_#000] my-2 max-w-md w-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b-2 border-black pb-2.5 mb-2.5">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-[#ffd700] border-2 border-black flex items-center justify-center font-bold text-sm shadow-[2px_2px_0px_#000]">
            ⭐
          </div>
          <div>
            <h4 className="text-xs font-bold mario-font text-slate-900 tracking-wider">
              MISSION #{data.mission_id}
            </h4>
            <span
              className={`text-[10px] font-bold px-2 py-0.5 rounded border ${getCategoryBadgeColor(
                data.category
              )}`}
            >
              {data.category || "Civic Issue"}
            </span>
          </div>
        </div>
        <span className="text-[10px] mario-font font-bold px-2 py-1 rounded bg-[#00a800] text-white border-2 border-black shadow-[1px_1px_0px_#000]">
          {data.status}
        </span>
      </div>

      {/* Description */}
      {data.description && (
        <p className="text-xs text-slate-800 font-medium mb-3 bg-slate-50 p-2 rounded-xl border border-slate-300">
          {data.description}
        </p>
      )}

      {/* Details Grid */}
      <div className="grid grid-cols-2 gap-2 text-xs mb-3">
        <div className="bg-[#e6f9ed] border-2 border-black p-2 rounded-xl shadow-[2px_2px_0px_#000]">
          <span className="text-[9px] mario-font text-[#00a800] block mb-0.5">SQUAD</span>
          <span className="font-bold text-slate-900 text-xs">{data.team || "Holkar Heroes"}</span>
        </div>
        <div className="bg-[#fff8db] border-2 border-black p-2 rounded-xl shadow-[2px_2px_0px_#000]">
          <span className="text-[9px] mario-font text-amber-700 block mb-0.5">WARD</span>
          <span className="font-bold text-slate-900 text-xs">{data.ward || "Ward 7"}</span>
        </div>
      </div>

      {/* Retro Mario TIME Countdown */}
      <div className="bg-black text-white p-2.5 rounded-xl border-2 border-black flex items-center justify-between shadow-[2px_2px_0px_#000]">
        <div className="flex items-center space-x-1.5 text-xs text-[#ffd700] mario-font">
          <span>TIME</span>
        </div>
        <div className="mario-font text-sm text-[#ffd700] tracking-widest font-bold">
          {formatRelativeTime(remainingSecs)}
        </div>
      </div>

      {/* Updates log if available */}
      {data.updates && data.updates.length > 0 && (
        <div className="mt-2.5 pt-2 border-t-2 border-slate-200">
          <span className="text-[9px] mario-font text-slate-600 block mb-1">
            LATEST ACTION:
          </span>
          <div className="text-xs text-slate-800 bg-slate-100 border border-black p-2 rounded-lg font-medium">
            {data.updates[data.updates.length - 1].update_text}
          </div>
        </div>
      )}
    </div>
  );
}
