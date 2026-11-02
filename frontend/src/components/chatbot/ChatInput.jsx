import React, { useState } from "react";
import { Send, MapPin, Navigation, X } from "lucide-react";
import ImageUploader from "./ImageUploader";
import VoiceRecorder from "./VoiceRecorder";

export default function ChatInput({
  sessionId,
  onSendMessage,
  onImageUploaded,
  onVoiceTranscribed,
  loading
}) {
  const [text, setText] = useState("");
  const [coordinates, setCoordinates] = useState(null);
  const [geoLocating, setGeoLocating] = useState(false);

  const handleSend = () => {
    if (!text.trim() || loading) return;
    onSendMessage(text.trim(), coordinates);
    setText("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleGetLocation = () => {
    if (coordinates) {
      setCoordinates(null);
      return;
    }

    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }

    setGeoLocating(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setCoordinates({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        });
        setGeoLocating(false);
      },
      (err) => {
        console.warn("Could not get exact GPS, using Ward 7 default:", err);
        setCoordinates({ latitude: 28.6139, longitude: 77.2090 });
        setGeoLocating(false);
      },
      { timeout: 8000 }
    );
  };

  return (
    <div className="bg-[#ffffff] border-t-3 border-black p-3">
      {/* GPS Location pill if active */}
      {coordinates && (
        <div className="mb-2 flex items-center justify-between bg-[#fff8db] border-2 border-black text-amber-900 text-xs px-3 py-1 rounded-lg font-bold shadow-[2px_2px_0px_#000]">
          <div className="flex items-center gap-1.5">
            <Navigation className="w-3.5 h-3.5 text-rose-600 animate-pulse" />
            <span>
              GPS Pinned: ({coordinates.latitude.toFixed(4)}, {coordinates.longitude.toFixed(4)})
            </span>
          </div>
          <button
            onClick={() => setCoordinates(null)}
            className="text-slate-600 hover:text-black font-bold"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Input controls */}
      <div className="flex items-center gap-1.5 bg-slate-50 border-2 border-black rounded-xl p-1.5 shadow-[2px_2px_0px_#000] focus-within:border-[#e52521]">
        {/* Camera / Image Upload */}
        <ImageUploader sessionId={sessionId} onUploaded={onImageUploaded} />

        {/* Voice Note Recorder */}
        <VoiceRecorder
          sessionId={sessionId}
          onTranscriptionComplete={(transcribed) => {
            setText(transcribed);
            if (onVoiceTranscribed) onVoiceTranscribed(transcribed);
          }}
        />

        {/* GPS Pin Button */}
        <button
          onClick={handleGetLocation}
          className={`p-2 rounded-lg transition border-2 cursor-pointer ${
            coordinates
              ? "bg-[#00a800] text-white border-black shadow-[1px_1px_0px_#000]"
              : "bg-white text-slate-700 border-black hover:bg-slate-100 shadow-[1px_1px_0px_#000]"
          }`}
          title={coordinates ? "GPS Location Pinned" : "Attach Current GPS Coordinates"}
        >
          <MapPin className={`w-4 h-4 ${geoLocating ? "animate-spin" : ""}`} />
        </button>

        {/* Text Input */}
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Apni samasya batayein (e.g. 'Naala overflow ho raha hai' / 'Pothole on Main Road')..."
          disabled={loading}
          className="flex-1 bg-transparent text-slate-900 placeholder-slate-400 text-xs sm:text-sm font-semibold px-2 py-1.5 focus:outline-none"
        />

        {/* Question Mark Yellow / Green Send Button */}
        <button
          onClick={handleSend}
          disabled={!text.trim() || loading}
          className="bg-[#ffd700] hover:bg-[#ffc800] text-black border-2 border-black px-3 py-1.5 rounded-lg font-bold text-xs mario-font shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 disabled:opacity-40 transition cursor-pointer flex items-center gap-1"
          title="Send"
        >
          <span>GO!</span>
          <Send className="w-3.5 h-3.5 ml-0.5" />
        </button>
      </div>
    </div>
  );
}
