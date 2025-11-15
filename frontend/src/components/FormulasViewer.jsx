import React, { useEffect, useState } from "react";
import { BlockMath } from "react-katex";
import "katex/dist/katex.min.css";
import "../styles/FormulasViewer.css";
import { loadFormulas } from "../services/api";

const FormulasViewer = ({ onInsert }) => {
  const [search, setSearch] = useState("");
  const [formulas, setFormulas] = useState([]);

  useEffect(() => {
    loadFormulas()
      .then((data) => {
        const categories = Object.entries(data.formulas || {}).map(
          ([name, formulas]) => ({
            name,
            formulas: Array.isArray(formulas) ? formulas : [],
          })
        );
        setFormulas(categories);
      })
      .catch((err) => console.error("Error loading formulas:", err));
  }, []);

  const filteredCategories = formulas
    .map((category) => ({
      ...category,
      formulas: (category.formulas || []).filter(
        (item) =>
          item.display_name.toLowerCase().includes(search.toLowerCase()) ||
          category.name.toLowerCase().includes(search.toLowerCase())
      ),
    }))
    .filter((category) => category.formulas.length > 0);

  return (
    <div className="formulas-wrapper">
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
          <div key={cat.name} className="formula-category">
            <h3>{cat.name}</h3>

            {cat.formulas.map((item) => (
              <div
                key={item.box_name}
                className="formula-item"
                onClick={() => onInsert(item.box_name)}
              >
                <strong>{item.display_name}</strong>
                <BlockMath math={item.latex_str} />
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FormulasViewer;
