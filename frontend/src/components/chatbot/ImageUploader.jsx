import React, { useState } from "react";
import { Camera, Image as ImageIcon, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { uploadImage } from "../../services/uploadApi";

export default function ImageUploader({ sessionId, onUploaded }) {
  const [uploading, setUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Local preview
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result);
    reader.readAsDataURL(file);

    try {
      setUploading(true);
      const res = await uploadImage(file, sessionId);
      if (res.success) {
        setAnalysisResult(res.analysis);
        if (onUploaded) onUploaded(res);
      }
    } catch (err) {
      console.error("Image upload failed", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="relative">
      <label className="flex items-center justify-center p-2 rounded-xl text-slate-400 hover:text-indigo-400 hover:bg-slate-800 transition cursor-pointer" title="Attach Civic Photo (YOLO & Vision AI)">
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFile}
          disabled={uploading}
          className="hidden"
        />
        {uploading ? (
          <Loader2 className="w-5 h-5 animate-spin text-indigo-400" />
        ) : (
          <Camera className="w-5 h-5" />
        )}
      </label>
    </div>
  );
}

