import React from "react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";

function ChatWindow({ messages, input, setInput, onSend, loading }) {
  return (
    <div className="app-container">
      <header>
        <h1>Conversational AI Agent</h1>
      </header>
      <main>
        <MessageList messages={messages} />
        <UserInput input={input} setInput={setInput} onSend={onSend} loading={loading} />
      </main>
    </div>
  );
}

export default ChatWindow;
