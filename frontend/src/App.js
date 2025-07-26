import React from "react";
import { ChatProvider, useChat } from "./ChatContext";
import ChatWindow from "./ChatWindow";
import "./App.css";

function AppContent() {
  const { messages, input, setInput, sendMessage, loading } = useChat();
  return (
    <ChatWindow
      messages={messages}
      input={input}
      setInput={setInput}
      onSend={sendMessage}
      loading={loading}
    />
  );
}

function App() {
  return (
    <ChatProvider>
      <AppContent />
    </ChatProvider>
  );
}

export default App;
