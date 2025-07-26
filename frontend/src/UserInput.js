import React from "react";

function UserInput({ input, setInput, onSend, loading }) {
  return (
    <form className="chat-input" onSubmit={onSend}>
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
  );
}

export default UserInput;
