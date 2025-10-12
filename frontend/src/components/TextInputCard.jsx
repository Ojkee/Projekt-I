import { useState, useEffect } from "react";
import { sendText } from "../services/api";

function TextInputCard({ cellId, value, onChange, onRemove, showControls = false }) {
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // Nasłuchiwanie eventu uruchomienia komórki z paska narzędzi
  useEffect(() => {
    const handleRunCell = (event) => {
      if (event.detail.cellId === cellId) {
        handleSend();
      }
    };

    window.addEventListener('runCell', handleRunCell);
    return () => window.removeEventListener('runCell', handleRunCell);
  }, [cellId, value]);

  const handleSend = async () => {
    const text = value.trim();
    if (!text) return;

    setLoading(true);
    setMessage("");

    try {
      const data = await sendText(text);
      setMessage(data.message || "✅ Wykonano pomyślnie");
    } catch (err) {
      setMessage("⚠️ Błąd połączenia z backendem");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="w-full">
      {/* Pole wprowadzania */}
      <div className="mb-3">
        <textarea
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={`Wprowadź kod lub tekst...`}
          className="w-full border border-gray-300 rounded-lg px-4 py-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent font-mono text-sm resize-y min-h-[100px]"
          rows={4}
        />
        <div className="text-xs text-gray-500 mt-1">
          Ctrl + Enter aby uruchomić komórkę
        </div>
      </div>

      {/* Kontrolki - tylko jeśli showControls=true */}
      {showControls && (
        <div className="flex gap-2 mb-3">
          <button
            onClick={handleSend}
            disabled={loading || !value.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
          >
            {loading ? "Wysyłanie..." : "Uruchom"}
          </button>
          <button
            onClick={onRemove}
            className="px-4 py-2 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600 text-sm font-medium"
          >
            Usuń
          </button>
        </div>
      )}

      {/* Output */}
      {message && (
        <div className="mt-3 p-3 bg-gray-50 border border-gray-200 rounded-lg">
          <div className="text-sm text-gray-600 mb-1 font-medium">Output:</div>
          <div className="text-gray-800 font-mono text-sm whitespace-pre-wrap">
            {message}
          </div>
        </div>
      )}
      
      {/* Stan ładowania */}
      {loading && (
        <div className="mt-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="text-sm text-blue-600 font-medium">
            ⏳ Wykonywanie komórki...
          </div>
        </div>
      )}
    </div>
  );
}

export default TextInputCard;