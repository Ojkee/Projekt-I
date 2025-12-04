import React, { useState, useEffect } from "react";
import CodeCell from "../components/CodeCell";
import FormulasViewer from "../components/FormulasViewer";
import "../styles/UserPage.css";
import { useNavigate } from "react-router-dom";
import { v4 as uuidv4 } from 'uuid';

function UserPage() {
  const [cells, setCells] = useState(() => {
  const saved = localStorage.getItem("cells");
    return saved ? JSON.parse(saved) : [{ id: uuidv4(), content: "" }];
  });

  const [activeCellId, setActiveCellId] = useState(
    () => cells[0]?.id || null
  );

  useEffect(() => {
    localStorage.setItem("cells", JSON.stringify(cells));
  }, [cells]);

  const updateCellContent = (id, newContent) => {
  setCells(prev =>
    prev.map(cell =>
      cell.id === id ? { ...cell, content: newContent } : cell
    )
  );
};

  const addCell = () => {
    const newCell = { id: uuidv4(), content: "" };
    setCells(prev => [...prev, newCell]);
    setActiveCellId(newCell.id);
  };

  const removeCell = (id) => {
    if (cells.length > 1) setCells(cells.filter((c) => c.id !== id));
  };

  const runAll = () => {
    window.dispatchEvent(new CustomEvent("runAllCells"));
  };

  const clearAll = () => {
    const fresh = [{ id: uuidv4(), content: "" }];
    setCells(fresh);
    setActiveCellId(fresh[0].id);
  };

  const insertFormula = (f_name) => {
    if (!activeCellId) return;
    const event = new CustomEvent("insertFormula", { detail: { cellId: activeCellId, f_name} });
    window.dispatchEvent(event);
  };

  const navigate = useNavigate();

  const [menuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
  setMenuOpen(!menuOpen);
};

  return (
    <div className="userpage-container">
      <header className="userpage-toolbar">
        <div className="userpage-toolbar-inner">
          <div className="toolbar-left">
          <button className="back-btn" onClick={() => navigate("/") } title="Back">
            <svg className="back-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24" >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back
          </button>
        </div>
          <h1 className="logo-text">Matika</h1>

          <div className="toolbar-right">
            <button onClick={runAll} className="run-all-btn" title="Run all">
              <svg className="run-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /> 
              </svg>
              Run all</button>
            <button onClick={addCell} className="add-cell-btn" title="Add">
              <svg className="add-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              Add</button>
            <button onClick={clearAll} className="remove-all-btn" title="Delete all">
              <svg className="remove-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              Delete all</button>
            <button 
              className={`toolbar-hamburger ${menuOpen ? "active" : ""}`}
              onClick={toggleMenu}
            >
              <span></span>
              <span></span>
              <span></span>
            </button>

            <div className={`toolbar-menu ${menuOpen ? "open" : ""}`}>
              <button onClick={addCell} className="add-cell-btn">Add</button>
              <button onClick={runAll} className="run-all-btn">Run all</button>
              <button onClick={clearAll} className="remove-all-btn">Delete all</button>
            </div>
          </div>
        </div>
      </header> 
      <main className="userpage-main">
        <div className="codecells-column">
          {cells.map((cell, idx) => (
            <CodeCell
              key={cell.id}
              cellId={cell.id}
              onRemove={removeCell}
              content={cell.content}
              onChange={updateCellContent}
              isRemovable={idx !== 0}
              onFocus={() => setActiveCellId(cell.id)} 
            />
          ))}
        </div>
        <div className="formulas-column">
        <FormulasViewer onInsert={insertFormula} />
        </div>
      </main>
    </div>
  );
}

export default UserPage;
