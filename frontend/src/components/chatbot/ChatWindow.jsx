import React, { useState, useEffect, useRef } from "react";
import ChatHeader from "./ChatHeader";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import QuickActions from "./QuickActions";
import TypingIndicator from "./TypingIndicator";
import ErrorMessage from "../common/ErrorMessage";
import { sendMessage, loginDemoUser, fetchRewards } from "../../services/chatApi";

export default function ChatWindow() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      message:
        "🍄 **IT'S-A ME, CITY GUARDIAN!**\n\nWelcome to your Super Civic Assistant! Aap kisi bhi civic samasya (sadak ka gaddha, nali overflow, kachre ka dher, ya broken streetlight) ki report **Hindi**, **English**, ya **Hinglish** me darj kar sakte hain, live squad tracking kar sakte hain, aur har complaint par **+15 COINS** 🪙 earn kar sakte hain!\n\nMain aapki kya madad karoon?",
    },
  ]);

  const [sessionId, setSessionId] = useState(
    () => `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`
  );
  const [currentUser, setCurrentUser] = useState({ id: 1, name: "Rahul Sharma", role: "CITIZEN" });
  const [rewards, setRewards] = useState({ points: 180, badge: "Active Citizen" });
  const [loading, setLoading] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);
  const [error, setError] = useState(null);

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    loadUserPersona(1);
  }, []);

  const loadUserPersona = async (userId) => {
    try {
      const authRes = await loginDemoUser(userId);
      if (authRes.success) {
        setCurrentUser(authRes.user);
        const rewRes = await fetchRewards();
        if (rewRes.success) {
          setRewards(rewRes);
        }
      }
    } catch (e) {
      console.warn("Could not login demo user:", e);
    }
  };

  const handleSendMessage = async (text, coordinates = null) => {
    if (!text.trim() || loading) return;

    const userMsg = {
      role: "user",
      message: text,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const res = await sendMessage(text, sessionId, coordinates);
      if (res.success) {
        const botMsg = {
          role: "assistant",
          message: res.response,
          metadata: {
            type: res.type,
            data: res.data,
          },
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, botMsg]);

        if (res.type === "REWARD_STATUS" || res.type === "COMPLAINT_CONFIRMED") {
          const updatedRew = await fetchRewards();
          if (updatedRew.success) setRewards(updatedRew);
        }
      } else {
        setError(res.error || "Unable to process request.");
      }
    } catch (err) {
      console.error("Chat error:", err);
      setError("Network or server connection error. Please ensure backend is running.");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          message: "Kshama karein, server se sampark sthapit nahi ho saka. Kripya punah prayas karein.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleImageUploaded = (uploadRes) => {
    const analysis = uploadRes.analysis;
    const cat = analysis?.primary_category || "civic issue";
    handleSendMessage(`Maine photo upload ki hai. Vision analysis me ${cat} mila hai.`);
  };

  const handleVoiceTranscribed = (transcription) => {
    handleSendMessage(transcription);
  };

  const handleConfirmComplaint = async () => {
    setLoadingAction(true);
    await handleSendMessage("Haan, confirm karo. Shikayat darj karein.");
    setLoadingAction(false);
  };

  const handleCancelComplaint = async () => {
    await handleSendMessage("Nahi, cancel kar do.");
  };

  const handleTrackMission = async (missionId) => {
    await handleSendMessage(`Track Mission #${missionId}`);
  };

  const handleProceedAnyway = async () => {
    await handleSendMessage("Yeh alag issue hai, kripya alag complaint draft banayein.");
  };

  const handleResetSession = () => {
    const newSession = `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    setSessionId(newSession);
    setMessages([
      {
        role: "assistant",
        message:
          "🍄 Level Reset! Welcome back. Main aapki kya madad kar sakta hoon?",
      },
    ]);
  };

  return (
    <div className="flex flex-col h-[82vh] max-w-4xl mx-auto w-full bg-[#f8fafc] border-4 border-black rounded-2xl shadow-[6px_6px_0px_#000] overflow-hidden">
      {/* Header */}
      <ChatHeader
        currentUser={currentUser}
        rewards={rewards}
        onResetSession={handleResetSession}
        onUserSwitch={loadUserPersona}
      />

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-[#eef2f6]">
        {messages.map((msg, index) => (
          <ChatMessage
            key={index}
            message={msg}
            onConfirmComplaint={handleConfirmComplaint}
            onCancelComplaint={handleCancelComplaint}
            onTrackMission={handleTrackMission}
            onProceedAnyway={handleProceedAnyway}
            onCouponRedeemed={(res) => {
              if (res.remaining_points !== undefined) {
                setRewards((prev) => ({ ...prev, points: res.remaining_points }));
              }
            }}
            loadingAction={loadingAction}
          />
        ))}

        {loading && <TypingIndicator />}
        {error && <ErrorMessage message={error} />}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Quick Actions */}
      <QuickActions onSelectAction={(act) => handleSendMessage(act)} />

      {/* Input bar */}
      <ChatInput
        sessionId={sessionId}
        onSendMessage={handleSendMessage}
        onImageUploaded={handleImageUploaded}
        onVoiceTranscribed={handleVoiceTranscribed}
        loading={loading}
      />
    </div>
  );
}
