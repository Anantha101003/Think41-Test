import React from "react";
import { ChatProvider, useChat } from "./ChatContext";
import ChatWindow from "./ChatWindow";
import "./App.css";

function AppContent() {
  return <ChatWindow />;
}

function App() {
  return (
    <ChatProvider>
      <AppContent />
    </ChatProvider>
  );
}

export default App;
