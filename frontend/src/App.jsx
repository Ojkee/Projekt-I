import React, { useState } from "react";
import CodeCell from "./components/CodeCell";

function App() {
  const [cells, setCells] = useState([{ id: 1 }]);

  const addCell = (afterId) => {
    const newId = Math.max(...cells.map(c => c.id)) + 1;
    const index = cells.findIndex(c => c.id === afterId);
    const newCells = [...cells];
    newCells.splice(index + 1, 0, { id: newId });
    setCells(newCells);
  };

  const removeCell = (id) => {
    setCells(cells.filter(c => c.id !== id));
  };

  return (
    <div style={{ padding: "20px", background: "#121212", minHeight: "100vh", minWidth: "300px" }}>
      <h1 style={{ color: "#fff", fontFamily: "monospace", marginBottom: "20px" }}>
        Interpreter
      </h1>

      {cells.map(c => (
        <CodeCell
          key={c.id}
          cellId={c.id}
          onAdd={addCell}
          onRemove={removeCell}
        />
      ))}
    </div>
  );
}

export default App;
