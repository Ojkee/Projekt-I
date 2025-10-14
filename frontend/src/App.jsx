import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    setLoading(true);
    setMessage("");

    try {
      const res = await fetch("http://localhost:8080/interpret", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: input }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setMessage(data.message);
    } catch (err) {
      setMessage("⚠️ Error connecting to backend");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-4">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Wpisz treść..."
        className="border rounded-xl px-3 py-2 w-64 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
      />

      <button
        onClick={handleSend}
        disabled={loading || !input.trim()}
        className="px-4 py-2 bg-blue-500 text-white rounded-xl shadow-md hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? "Wysyłanie..." : "Wyślij"}
      </button>

      {message && (
        <p className="text-lg text-gray-700 font-medium">{message}</p>
      )}
    </div>
  );
}

export default App;
