import React, { useState } from "react";
import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "../styles/FormulasViewer.css"

const FormulasColumn = ({ formulas, onInsert }) => {
  const [search, setSearch] = useState("");

  const filteredCategories = formulas
    .map((category) => ({
      ...category,
      items: category.items.filter(
        (item) =>
          item.name.toLowerCase().includes(search.toLowerCase()) ||
          category.category.toLowerCase().includes(search.toLowerCase())
      ),
    }))
    .filter((category) => category.items.length > 0);

  return (
    <div className="formulas-container">
      <input
        type="text"
        placeholder="Szukaj wzoru..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="formula-search"
      />

      {filteredCategories.map((cat) => (
        <div key={cat.category} className="formula-category">
          <h3>{cat.category}</h3>

          {cat.items.map((item) =>
            Array.isArray(item.latex) ? (
              item.latex.map((eq, i) => (
                <div
                  key={i}
                  className="formula-item"
                  onClick={() => onInsert(eq)}
                >
                  <strong>{item.name}</strong>
                  <BlockMath math={eq} />
                </div>
              ))
            ) : (
              <div
                key={item.name}
                className="formula-item"
                onClick={() => onInsert(item.latex)}
              >
                <strong>{item.name}</strong>
                <BlockMath math={item.latex} />
              </div>
            )
          )}
        </div>
      ))}
    </div>
  );
};

export default FormulasColumn;
