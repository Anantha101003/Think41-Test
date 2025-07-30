import React from "react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";
import ConversationHistoryPanel from "./ConversationHistoryPanel";
import { useChat } from "./ChatContext";
import "./ChatWindow.css";

function ChatWindow() {
  const { messages, input, setInput, sendMessage, loading, sessions, conversationId, loadSession } = useChat();
  return (
    <div className="app-container chat-layout">
      <ConversationHistoryPanel sessions={sessions} onSelect={loadSession} currentId={conversationId} />
      <div className="chat-main">
        <header>
          <h1>Conversational AI Agent</h1>
        </header>
        <main>
          <MessageList messages={messages} />
          <UserInput input={input} setInput={setInput} onSend={sendMessage} loading={loading} />
        </main>
      </div>
    </div>
  );
}

export default ChatWindow;
