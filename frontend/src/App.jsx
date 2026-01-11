import React, { useState } from "react";
import { askQuestion } from "./api";

import QueryInput from "./components/QueryInput";
import AnswerCard from "./components/AnswerCard";
import SourcesList from "./components/SourcesList";
import WarningBanner from "./components/WarningBanner";
// import FeedbackButtons from "./components/FeedbackButtons"; // disabled for now

export default function App() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleAsk = async (query) => {
    try {
      setLoading(true);
      setError(null);
      setResponse(null);

      const data = await askQuestion(query);

      console.log("Backend response:", data); // 🔥 Debug proof

      setResponse(data);
    } catch (err) {
      console.error("Error asking question:", err);
      setError("Failed to fetch response from backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ padding: "30px" }}>
      <h1>🧘 Ask Me Anything About Yoga</h1>

      <QueryInput onAsk={handleAsk} />

      {loading && <p className="loading">Thinking...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {response && (
        <>
          {response.isUnsafe && (
            <WarningBanner message={response.warning} />
          )}

          <AnswerCard answer={response.answer} />

          <SourcesList sources={response.sources} />

          {/* Feedback disabled until backend supports queryId */}
          {/* <FeedbackButtons queryId={response.queryId} /> */}
        </>
      )}
    </div>
  );
}
