import React from "react";
import { AlertCircle } from "lucide-react";

export default function ErrorMessage({ message }) {
  if (!message) return null;
  return (
    <div className="flex items-center space-x-2 bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs px-3 py-2 rounded-xl my-2">
      <AlertCircle className="w-4 h-4 flex-shrink-0" />
      <span>{message}</span>
    </div>
  );
}

