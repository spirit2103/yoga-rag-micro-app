import React from "react";

export default function AnswerCard({ answer }) {
  if (!answer) return null;

  return (
    <div className="answer-card">
      <h2>AI Answer</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>
        {answer}
      </pre>
    </div>
  );
}
