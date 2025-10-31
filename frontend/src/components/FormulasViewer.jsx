import React, { useState } from "react";
import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "../styles/FormulasViewer.css"

const FormulasViewer = ({ formulas = [], onInsert }) => {
  const [search, setSearch] = useState("");

  const formulaList = Array.isArray(formulas) ? formulas : [];

  const filtered = formulaList.filter(
    (f) =>
      f.name.toLowerCase().includes(search.toLowerCase()) ||
      f.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="formulas-container">
      <input
        type="text"
        placeholder="Szukaj wzoru..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="formula-search"
      />

      {filtered.length === 0 && <p>Brak wyników</p>}

      {filtered.map((f) => (
        <div
          key={f.id}
          onClick={() => onInsert(f.latex)}
        >
          <strong>{f.name}</strong> <em>({f.category})</em>
          <BlockMath math={f.latex} />
        </div>
      ))}
    </div>
  );
};

export default FormulasViewer;
