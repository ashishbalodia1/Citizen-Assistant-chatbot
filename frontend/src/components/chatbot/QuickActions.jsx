import React from "react";

export default function QuickActions({ onSelectAction }) {
  const actions = [
    { label: "Naala overflow ho raha hai", icon: "🌊", bg: "bg-[#e8f4fd] text-[#0066cc]" },
    { label: "Track Mission #7042", icon: "⭐", bg: "bg-[#fff8db] text-[#b38600]" },
    { label: "Mere points kitne hain?", icon: "🪙", bg: "bg-[#fdf0ed] text-[#e52521]" },
    { label: "Deep pothole on Main Road", icon: "🚧", bg: "bg-[#f4faee] text-[#00a800]" },
    { label: "Show available local coupons", icon: "🎁", bg: "bg-[#f7edf9] text-[#800080]" },
  ];

  return (
    <div className="py-2 px-3 flex items-center gap-2 overflow-x-auto no-scrollbar border-t-2 border-black bg-[#ffffff]">
      <span className="text-[9px] mario-font text-slate-500 whitespace-nowrap">
        ITEMS:
      </span>
      {actions.map((act, index) => (
        <button
          key={index}
          onClick={() => onSelectAction(act.label)}
          className={`flex items-center space-x-1.5 ${act.bg} hover:brightness-95 border-2 border-black text-xs font-bold px-2.5 py-1 rounded-lg whitespace-nowrap shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer`}
        >
          <span>{act.icon}</span>
          <span>{act.label}</span>
        </button>
      ))}
    </div>
  );
}
