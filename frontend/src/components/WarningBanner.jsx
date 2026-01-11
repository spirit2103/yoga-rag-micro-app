import React from "react";

export default function WarningBanner({ message }) {
  return (
    <div className="warning">
      ⚠️ {message}
      <p>Please consult a certified yoga therapist or doctor.</p>
    </div>
  );
}
