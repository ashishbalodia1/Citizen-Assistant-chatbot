import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Volume2, CheckCircle2 } from "lucide-react";
import { speakMessage } from "../../services/voiceApi";
import MissionCard from "../cards/MissionCard";
import ComplaintCard from "../cards/ComplaintCard";
import RewardCard from "../cards/RewardCard";
import DuplicateAlert from "../cards/DuplicateAlert";

export default function ChatMessage({
  message,
  onConfirmComplaint,
  onCancelComplaint,
  onTrackMission,
  onProceedAnyway,
  onCouponRedeemed,
  loadingAction
}) {
  const isUser = message.role === "user";
  const [speaking, setSpeaking] = useState(false);

  const handleSpeak = () => {
    setSpeaking(true);
    speakMessage(message.message || message.text || "");
    setTimeout(() => setSpeaking(false), 3000);
  };

  const metadata = message.metadata;
  const cardType = metadata?.type;
  const cardData = metadata?.data;

  return (
    <div
      className={`flex items-start gap-2.5 my-2.5 ${
        isUser ? "flex-row-reverse" : "flex-row"
      } max-w-[95%] sm:max-w-[85%] ${isUser ? "ml-auto" : "mr-auto"}`}
    >
      {/* Avatar */}
      <div
        className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 text-sm font-bold border-2 border-black shadow-[2px_2px_0px_#000] ${
          isUser
            ? "bg-[#00a800] text-white"
            : "bg-[#e52521] text-white"
        }`}
      >
        {isUser ? "🧑" : "🍄"}
      </div>

      {/* Bubble & Cards */}
      <div className="flex flex-col gap-1.5 w-full">
        <div
          className={`px-4 py-3 rounded-2xl text-xs sm:text-sm leading-relaxed relative ${
            isUser
              ? "bg-[#00a800] text-white border-2 border-black shadow-[3px_3px_0px_#000] rounded-tr-none ml-auto font-medium"
              : "bg-white text-slate-900 border-2 border-black shadow-[3px_3px_0px_#000] rounded-tl-none font-medium"
          }`}
        >
          {/* Markdown Content */}
          <div className="prose prose-xs max-w-none text-inherit">
            <ReactMarkdown>
              {message.message || message.text || ""}
            </ReactMarkdown>
          </div>

          {/* Speech Button for Assistant Message */}
          {!isUser && (
            <div className="flex items-center justify-between mt-2 pt-1.5 border-t border-slate-200 text-[11px] text-slate-500 font-semibold">
              <span className="text-[10px] mario-font text-[#e52521]">CITY GUARDIAN</span>
              <button
                onClick={handleSpeak}
                className="flex items-center gap-1 text-slate-600 hover:text-black bg-slate-100 hover:bg-slate-200 px-2 py-0.5 rounded border border-black shadow-[1px_1px_0px_#000] transition cursor-pointer"
                title="Voice output"
              >
                <Volume2 className={`w-3.5 h-3.5 text-[#e52521] ${speaking ? "animate-pulse" : ""}`} />
                <span>Listen</span>
              </button>
            </div>
          )}
        </div>

        {/* Structured Interactive Cards */}
        {cardType === "MISSION_STATUS" && (
          <MissionCard data={cardData} />
        )}

        {cardType === "COMPLAINT_DRAFT" && (
          <ComplaintCard
            data={cardData}
            onConfirm={onConfirmComplaint}
            onCancel={onCancelComplaint}
            loading={loadingAction}
          />
        )}

        {cardType === "COMPLAINT_CONFIRMED" && (
          <div className="bg-[#e6f9ed] border-2 border-black shadow-[3px_3px_0px_#000] rounded-xl p-3 my-1.5 text-xs text-emerald-900 flex items-center space-x-2">
            <CheckCircle2 className="w-5 h-5 text-[#00a800] flex-shrink-0" />
            <div>
              <span className="font-bold mario-font text-[10px] text-[#00a800] block mb-0.5">LEVEL COMPLETE!</span>
              <span>Complaint verified & registered. Squad dispatched!</span>
            </div>
          </div>
        )}

        {(cardType === "REWARD_STATUS" || cardType === "COUPON_LIST") && (
          <RewardCard data={cardData} onCouponRedeemed={onCouponRedeemed} />
        )}

        {cardType === "DUPLICATE_ALERT" && (
          <DuplicateAlert
            data={cardData}
            onTrackExisting={onTrackMission}
            onProceedAnyway={onProceedAnyway}
          />
        )}
      </div>
    </div>
  );
}
