import React from "react";
import "./Message.css";

function Message({ role, content, timestamp }) {
  return (
    <div className={`chat-message ${role}`} title={timestamp}>
      <span className="role">{role === "user" ? "You" : "AI"}:</span>
      <span className="content">{content}</span>
    </div>
  );
}

export default Message;
