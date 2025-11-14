import React, { useState } from "react";
import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "../styles/FormulasViewer.css"

const FormulasViewer = ({ formulas, onInsert }) => {
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
        <div className="formula-search-background">
        <input
          type="text"
          placeholder="Search formula..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="formula-search"
        />
        </div>

      {filteredCategories.map((cat) => (
        <div key={cat.category} className="formula-category">
          <h3>{cat.category}</h3>

          {cat.items.map((item) =>
            Array.isArray(item.latex) ? (
              item.latex.map((eq, i) => {
                const eqName = eq.eq_name || "";
                const eqLatex = eq.eq || eq;
                return (
                <div
                  key={i}
                  className="formula-item"
                  onClick={() => onInsert(eqName)}
                >
                  <strong>{item.name}</strong>
                    <BlockMath math={eqLatex} />
                  </div>
                );
              })
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

export default FormulasViewer;
