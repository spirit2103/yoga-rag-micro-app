import React, { useState } from "react";

export default function QueryInput({ onAsk }) {
  const [query, setQuery] = useState("");

  const submit = () => {
    if (query.trim()) onAsk(query);
  };

  return (
    <div className="query-box">
      <textarea
        placeholder="Ask anything about yoga..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={submit}>Ask</button>
    </div>
  );
}
