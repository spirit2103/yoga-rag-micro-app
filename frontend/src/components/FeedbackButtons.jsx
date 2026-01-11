import React from "react";
import { sendFeedback } from "../api";

export default function FeedbackButtons({ queryId }) {
  return (
    <div className="feedback">
      <span>Was this helpful?</span>
      <button onClick={() => sendFeedback(queryId, "up")}>👍</button>
      <button onClick={() => sendFeedback(queryId, "down")}>👎</button>
    </div>
  );
}
