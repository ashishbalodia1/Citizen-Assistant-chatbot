import React from "react";
import { RefreshCw } from "lucide-react";

export default function ChatHeader({
  currentUser,
  rewards,
  onResetSession,
  onUserSwitch
}) {
  return (
    <div className="bg-[#ffffff] border-b-4 border-black px-4 py-3 flex items-center justify-between shadow-sm">
      {/* Brand & Bot Status */}
      <div className="flex items-center space-x-3">
        <div className="relative">
          {/* Mario Cap / Mushroom Emblem */}
          <div className="w-11 h-11 rounded-xl bg-[#e52521] border-3 border-black flex items-center justify-center shadow-[3px_3px_0px_#000]">
            <span className="text-xl">🍄</span>
          </div>
          <span className="absolute -bottom-1 -right-1 w-3.5 h-3.5 bg-[#00a800] border-2 border-black rounded-full" />
        </div>

        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xs sm:text-sm font-black mario-font text-[#e52521] tracking-tight">
              CITY GUARDIAN
            </h1>
            <span className="bg-[#ffd700] text-black text-[9px] font-bold px-2 py-0.5 rounded border-2 border-black shadow-[1px_1px_0px_#000] mario-font">
              AI 2.5
            </span>
          </div>
          <p className="text-[11px] font-bold text-slate-600 flex items-center gap-1 mt-0.5">
            <span className="text-amber-500">★</span> Multilingual Civic Hero (Hindi / English / Hinglish)
          </p>
        </div>
      </div>

      {/* Citizen Profile Stats & Controls */}
      <div className="flex items-center space-x-2">
        {/* Coin / Points Tally */}
        {rewards && (
          <div className="hidden sm:flex items-center space-x-1.5 bg-[#fff8db] border-2 border-black px-2.5 py-1 rounded-lg text-xs font-bold shadow-[2px_2px_0px_#000]">
            <span className="text-base animate-bounce">🪙</span>
            <div>
              <span className="mario-font text-xs text-amber-700">{rewards.points || 0}</span>
              <span className="text-[9px] text-slate-600 block uppercase font-bold">{rewards.badge || "Guardian"}</span>
            </div>
          </div>
        )}

        {/* Persona Switcher */}
        <select
          value={currentUser?.id || 1}
          onChange={(e) => onUserSwitch && onUserSwitch(Number(e.target.value))}
          className="bg-white border-2 border-black text-slate-800 text-xs font-bold rounded-lg px-2 py-1.5 focus:outline-none shadow-[2px_2px_0px_#000] cursor-pointer"
          title="Switch Player Persona"
        >
          <option value={1}>Player 1: Rahul (Ward 7)</option>
          <option value={2}>Player 2: Priya (Ward 1)</option>
          <option value={3}>Officer: Inspector Gupta</option>
        </select>

        {/* Reset Session */}
        <button
          onClick={onResetSession}
          className="p-1.5 bg-slate-100 hover:bg-slate-200 border-2 border-black rounded-lg transition shadow-[2px_2px_0px_#000] cursor-pointer"
          title="Restart Level / Reset Session"
        >
          <RefreshCw className="w-4 h-4 text-slate-700" />
        </button>
      </div>
    </div>
  );
}
