const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8080/";

export async function sendText(code) {
  const res = await fetch(`${BACKEND_URL}/interpret`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ code }),
  });

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}

export async function loadFormulas() {
  const res = await fetch(`${BACKEND_URL}/get_formulas_json`);

  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }

  return res.json();
}