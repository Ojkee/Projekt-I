import { useState } from "react";
import TextInputCard from "../components/TextInputCard";

function UserPage() {
  const [cells, setCells] = useState([{ id: 1, content: "" }]);

  const handleChange = (id, value) => {
    setCells(cells.map(cell => 
      cell.id === id ? { ...cell, content: value } : cell
    ));
  };

  const addCell = () => {
    setCells([...cells, { id: Date.now(), content: "" }]);
  };

  const removeCell = (id) => {
    if (cells.length > 1) {
      setCells(cells.filter(cell => cell.id !== id));
    }
  };

  const runAll = () => {
    cells.forEach(cell => {
      const event = new CustomEvent('runCell', { detail: { cellId: cell.id } });
      window.dispatchEvent(event);
    });
  };

  const clearAll = () => {
    setCells([{ id: Date.now(), content: "" }]);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="bg-white rounded-lg shadow-md p-3 mb-4 flex items-center space-x-4 border-l-4 border-l-orange-500">
        <button
          onClick={runAll}
          className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex items-center space-x-2 text-sm font-medium"
        >
          <span>▶</span>
          <span>Uruchom wszystkie</span>
        </button>
        
        <button
          onClick={addCell}
          className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center space-x-2 text-sm font-medium"
        >
          <span>+</span>
          <span>Dodaj komórkę</span>
        </button>
        
        <button
          onClick={clearAll}
          className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600 flex items-center space-x-2 text-sm font-medium"
        >
          <span>×</span>
          <span>Wyczyść wszystkie</span>
        </button>
      </div>

      <div className="space-y-6">
        {cells.map((cell, index) => (
          <div key={cell.id} className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="flex items-center justify-between bg-gray-100 px-4 py-2 border-b">
              <div className="flex space-x-2">
                <button
                  onClick={() => {
                    const event = new CustomEvent('runCell', { detail: { cellId: cell.id } });
                    window.dispatchEvent(event);
                  }}
                  className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 text-sm flex items-center space-x-1"
                >
                  <span>▶</span>
                  <span>Uruchom</span>
                </button>
                <button
                  onClick={() => removeCell(cell.id)}
                  disabled={cells.length === 1}
                  className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm flex items-center space-x-1"
                >
                  <span>×</span>
                  <span>Usuń</span>
                </button>
              </div>
            </div>


            <div className="p-4">
              <TextInputCard
                cellId={cell.id}
                value={cell.content}
                onChange={(value) => handleChange(cell.id, value)}
                onRemove={() => removeCell(cell.id)}
                showControls={false} 
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default UserPage;