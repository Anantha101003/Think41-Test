import React from "react";
import Message from "./Message";

function MessageList({ messages }) {
  return (
    <div className="chat-window">
      {messages.length === 0 && <div className="empty-chat">Start the conversation!</div>}
      {messages.map((msg, idx) => (
        <Message key={idx} {...msg} />
      ))}
    </div>
  );
}

export default MessageList;
