import React, { createContext, useContext, useState, useRef, useEffect } from "react";

const ChatContext = createContext();

export function useChat() {
  return useContext(ChatContext);
}

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [userId, setUserId] = useState(() => localStorage.getItem("user_id") || "user-" + Math.random().toString(36).slice(2, 10));
  const [conversationId, setConversationId] = useState(null);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    localStorage.setItem("user_id", userId);
  }, [userId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, message: input, conversation_id: conversationId }),
      });
      if (!res.ok) throw new Error("API error");
      const data = await res.json();
      setConversationId(data.conversation_id);
      setMessages(data.messages);
      setInput("");
    } catch (err) {
      alert("Failed to send message: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        input,
        setInput,
        userId,
        setUserId,
        conversationId,
        setConversationId,
        loading,
        setLoading,
        sendMessage,
        messagesEndRef,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}
