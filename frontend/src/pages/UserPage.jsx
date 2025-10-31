import React, { useState } from "react";
import CodeCell from "../components/CodeCell";
import FormulasColumn from "../components/FormulasColumn";
import formulas from "../data/formulas.js";
import "../styles/UserPage.css";

function UserPage() {
  const [cells, setCells] = useState([{ id: Date.now() }]);
  const [activeCellId, setActiveCellId] = useState(cells[0].id);

  const addCell = () => {
    const newCell = { id: Date.now() };
    setCells([...cells, newCell]);
  };

  const removeCell = (id) => {
    if (cells.length > 1) setCells(cells.filter((c) => c.id !== id));
  };

  const runAll = () => {
    window.dispatchEvent(new CustomEvent("runAllCells"));
  };

  const clearAll = () => {
    setCells([{ id: Date.now() }]);
  };

  const insertFormula = (latex) => {
    if (!activeCellId) return;
    const event = new CustomEvent("insertFormula", { detail: { cellId: activeCellId, latex } });
    window.dispatchEvent(event);
  };

  return (
    <div className="userpage-container">
      <div className="userpage-toolbar">
        <button onClick={runAll} className="toolbar-btn primary">Run all</button>
        <button onClick={addCell} className="toolbar-btn">+</button>
        <button onClick={clearAll} className="toolbar-btn danger">Delete all</button>
      </div>

      <div className="userpage-main">
        <div className="codecells-column">
          {cells.map((cell, idx) => (
            <CodeCell
              key={cell.id}
              cellId={cell.id}
              onRemove={removeCell}
              isRemovable={idx !== 0}
              onFocus={() => setActiveCellId(cell.id)} 
            />
          ))}
        </div>

        <FormulasColumn formulas={formulas} onInsert={insertFormula} />
      </div>
    </div>
  );
}

export default UserPage;
