const API_BASE = "http://localhost:5000";

export async function askQuestion(query) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });
  return res.json();
}

export async function sendFeedback(queryId, feedback) {
  await fetch(`${API_BASE}/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ queryId, feedback })
  });
}
