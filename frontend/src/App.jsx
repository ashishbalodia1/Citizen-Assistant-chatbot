import React, { useState } from "react";
import ChatWindow from "./components/chatbot/ChatWindow";
import MunicipalHub from "./components/dashboard/MunicipalHub";
import { MessageSquare, ShieldCheck, Sparkles } from "lucide-react";

function App() {
  const [currentView, setCurrentView] = useState("CHAT"); // CHAT or OFFICER_HUB

  return (
    <div className="min-h-screen bg-[#5c94fc] flex flex-col justify-between relative overflow-hidden select-none">
      {/* Background Pixel Clouds */}
      <div className="absolute top-8 left-12 opacity-80 pointer-events-none hidden md:block">
        <div className="flex items-center space-x-1">
          <div className="w-16 h-8 bg-white border-2 border-black rounded-full" />
          <div className="w-24 h-12 bg-white border-2 border-black rounded-full -ml-8 -mt-4" />
          <div className="w-16 h-8 bg-white border-2 border-black rounded-full -ml-6" />
        </div>
      </div>

      <div className="absolute top-16 right-20 opacity-80 pointer-events-none hidden md:block">
        <div className="flex items-center space-x-1">
          <div className="w-14 h-7 bg-white border-2 border-black rounded-full" />
          <div className="w-20 h-10 bg-white border-2 border-black rounded-full -ml-6 -mt-3" />
          <div className="w-14 h-7 bg-white border-2 border-black rounded-full -ml-5" />
        </div>
      </div>

      {/* Top Super Mario Arcade Scoreboard Bar */}
      <header className="bg-black text-white px-4 py-2 border-b-4 border-black z-30">
        <div className="max-w-4xl mx-auto flex items-center justify-between text-xs mario-font tracking-wider">
          <div className="flex items-center space-x-3">
            <span className="text-[#e52521] font-bold text-sm">MARIO</span>
            <span className="text-white hidden sm:inline">CITY GUARDIAN</span>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1 text-[#ffd700]">
              <span className="inline-block animate-bounce">🪙</span>
              <span>x15 PTS</span>
            </div>
            <div className="hidden sm:block text-slate-300">
              WORLD <span className="text-white">1-1</span>
            </div>
          </div>

          {/* View Switcher */}
          <div className="flex items-center space-x-1 bg-slate-900 border-2 border-white rounded-lg p-0.5">
            <button
              onClick={() => setCurrentView("CHAT")}
              className={`flex items-center space-x-1 px-2 py-1 rounded text-[10px] mario-font transition cursor-pointer ${
                currentView === "CHAT"
                  ? "bg-[#e52521] text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <span>🍄 CHAT</span>
            </button>
            <button
              onClick={() => setCurrentView("OFFICER_HUB")}
              className={`flex items-center space-x-1 px-2 py-1 rounded text-[10px] mario-font transition cursor-pointer ${
                currentView === "OFFICER_HUB"
                  ? "bg-[#00a800] text-white shadow-sm"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              <span>🏰 PORTAL</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 flex flex-col justify-center py-2 px-2 sm:px-4 z-20">
        {currentView === "CHAT" ? (
          <ChatWindow onOpenOfficerHub={() => setCurrentView("OFFICER_HUB")} />
        ) : (
          <MunicipalHub onClose={() => setCurrentView("CHAT")} />
        )}
      </main>

      {/* Retro Mario Ground Platform */}
      <footer className="w-full h-12 mario-ground z-10 relative flex items-center justify-center">
        <span className="text-[10px] mario-font text-white/90 drop-shadow-[0_1px_1px_rgba(0,0,0,0.8)]">
          ★ SUPER MARIO CIVIC ASSISTANT – POWERED BY GEMINI AI ★
        </span>
      </footer>
    </div>
  );
}

export default App;
