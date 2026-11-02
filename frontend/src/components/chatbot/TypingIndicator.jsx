import React from "react";

export default function TypingIndicator() {
  return (
    <div className="flex items-start space-x-2 my-2 max-w-[85%]">
      <div className="w-9 h-9 rounded-xl bg-[#e52521] border-2 border-black flex items-center justify-center flex-shrink-0 text-white shadow-[2px_2px_0px_#000]">
        🍄
      </div>
      <div className="bg-white border-2 border-black rounded-2xl rounded-tl-none px-4 py-2.5 shadow-[3px_3px_0px_#000] flex items-center space-x-2">
        <span className="text-xs font-bold text-slate-700">Guardian Mario is thinking</span>
        <div className="w-2 h-2 rounded-full bg-[#e52521] animate-bounce" style={{ animationDelay: "0ms" }} />
        <div className="w-2 h-2 rounded-full bg-[#ffd700] animate-bounce" style={{ animationDelay: "150ms" }} />
        <div className="w-2 h-2 rounded-full bg-[#00a800] animate-bounce" style={{ animationDelay: "300ms" }} />
      </div>
    </div>
  );
}
