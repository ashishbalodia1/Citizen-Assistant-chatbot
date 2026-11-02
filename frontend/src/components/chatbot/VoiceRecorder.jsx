import React, { useState, useRef } from "react";
import { Mic, Square, Loader2, Volume2 } from "lucide-react";
import { uploadVoice } from "../../services/voiceApi";

export default function VoiceRecorder({ sessionId, onTranscriptionComplete }) {
  const [isRecording, setIsRecording] = useState(false);
  const [uploading, setUploading] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
        stream.getTracks().forEach((track) => track.stop());
        await handleAudioUpload(audioBlob);
      };

      mediaRecorder.start();
      setIsRecording(true);
    } catch (err) {
      console.error("Microphone access denied or error:", err);
      alert("Microphone access denied. Please grant microphone permission to record voice notes.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleAudioUpload = async (audioBlob) => {
    try {
      setUploading(true);
      const res = await uploadVoice(audioBlob, sessionId);
      if (res.success && res.transcription) {
        if (onTranscriptionComplete) {
          onTranscriptionComplete(res.transcription);
        }
      }
    } catch (error) {
      console.error("Voice upload failed:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex items-center">
      {isRecording ? (
        <button
          onClick={stopRecording}
          className="flex items-center space-x-1.5 bg-rose-600 hover:bg-rose-500 text-white text-xs px-2.5 py-1.5 rounded-xl transition duration-150 animate-pulse cursor-pointer"
          title="Stop & Transcribe Voice Note"
        >
          <Square className="w-3.5 h-3.5 fill-current" />
          <span>Recording... Stop</span>
        </button>
      ) : uploading ? (
        <div className="p-2 text-indigo-400">
          <Loader2 className="w-5 h-5 animate-spin" />
        </div>
      ) : (
        <button
          onClick={startRecording}
          className="p-2 text-slate-400 hover:text-indigo-400 hover:bg-slate-800 rounded-xl transition cursor-pointer"
          title="Record Hindi / English Voice Note (Whisper AI)"
        >
          <Mic className="w-5 h-5" />
        </button>
      )}
    </div>
  );
}

