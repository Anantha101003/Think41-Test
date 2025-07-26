import React, { useState, useRef, useEffect } from "react";
import "./App.css";

const API_URL = "http://localhost:8000/api/chat";

function App() {
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
      const res = await fetch(API_URL, {
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
    <div className="app-container">
      <header>
        <h1>Conversational AI Agent</h1>
      </header>
      <main>
        <div className="chat-window">
          {messages.length === 0 && <div className="empty-chat">Start the conversation!</div>}
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.role}`}>
              <span className="role">{msg.role === "user" ? "You" : "AI"}:</span>
              <span className="content">{msg.content}</span>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <form className="chat-input" onSubmit={sendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
            autoFocus
          />
          <button type="submit" disabled={loading || !input.trim()}>
            {loading ? "..." : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
