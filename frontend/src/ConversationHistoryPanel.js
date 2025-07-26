import React from "react";
import "./ConversationHistoryPanel.css";

function ConversationHistoryPanel({ sessions, onSelect, currentId }) {
  return (
    <aside className="history-panel">
      <h2>Conversations</h2>
      <ul>
        {sessions.length === 0 && <li className="empty">No conversations</li>}
        {sessions.map((session) => (
          <li
            key={session.id}
            className={session.id === currentId ? "active" : ""}
            onClick={() => onSelect(session.id)}
          >
            {session.title || `Session #${session.id}`}
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default ConversationHistoryPanel;
