import React from "react";

export default function SourcesList({ sources }) {
  return (
    <div className="card">
      <h4>Sources Used</h4>
      <ul>
        {sources.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}
