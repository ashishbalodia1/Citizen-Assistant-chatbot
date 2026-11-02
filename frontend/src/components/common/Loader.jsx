import React from "react";

export default function Loader({ text = "Processing..." }) {
  return (
    <div className="flex items-center space-x-2 text-slate-400 text-xs py-2">
      <div className="w-2 h-2 rounded-full bg-indigo-500 animate-ping" />
      <span className="font-medium text-slate-300">{text}</span>
    </div>
  );
}

