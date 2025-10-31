import React, { useState, useEffect } from "react";
import CodeEditor from "./CodeEditor";
import { LucidePlay, LucideTrash } from "lucide-react";
import { sendText } from "../services/api";

const CodeCell = ({ cellId, onRemove, isRemovable, onFocus }) => {
  const [code, setCode] = useState("");
  const [outputs, setOutputs] = useState([]);
  const [running, setRunning] = useState(false);

  const handleRun = async () => {
    if (!code.trim()) return;
    setRunning(true);
    const lines = code.split("\n").filter((l) => l.trim() !== "");
    const results = [];

    for (const line of lines) {
      try {
        const res = await sendText(line);
        let output = "";

        if (res && typeof res === "object") {
          if (typeof res.final === "string") output = res.final;
          else if (res.output) output = String(res.output);
          else if (Array.isArray(res.steps)) output = res.steps.join(", ");
          else output = JSON.stringify(res);
        } else {
          output = String(res);
        }

        results.push({ line, output });
      } catch (err) {
        console.error("Error on line:", line, err);
        results.push({ line, output: "❌ Error executing line" });
      }
    }

    setOutputs(results);
    setRunning(false);
  };

  useEffect(() => {
    const handler = (e) => {
      if (e.detail.cellId === cellId) setCode((prev) => prev + e.detail.latex);
    };
    window.addEventListener("insertFormula", handler);
    return () => window.removeEventListener("insertFormula", handler);
  }, [cellId]);

  useEffect(() => {
    const handleGlobalRun = () => handleRun();
    window.addEventListener("runAllCells", handleGlobalRun);
    return () => window.removeEventListener("runAllCells", handleGlobalRun);
  }, [code]);

  return (
    <div className="codecell" style={{ position: "relative", marginBottom: "20px" }}>
      {isRemovable && (
        <button
          onClick={() => onRemove && onRemove(cellId)}
          style={removeButtonStyle}
          title="Usuń komórkę"
        >
          X
        </button>
      )}

      <div onClick={() => onFocus && onFocus()} style={{ cursor: "text" }}>
        <CodeEditor value={code} onChange={setCode} />
      </div>

      <div className="codecell-buttons">
        <button onClick={handleRun} className="icon-btn" title="Uruchom">
          <LucidePlay size={16} />
          {running ? " Uruchamianie..." : ""}
        </button>
      </div>

      {outputs.length > 0 && (
        <div className="results">
          {outputs.map((item, i) => (
            <div key={i} className="result-line">
              <span className="result-step">{item.line}</span>
              <span className="result-value">{item.output}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const removeButtonStyle = {
  position: "absolute",
  top: "8px",
  right: "8px",
  border: "none",
  background: "rgba(255,0,0,0.3)",
  color: "#fff",
  borderRadius: "50%",
  width: "28px",
  height: "28px",
  cursor: "pointer",
  fontWeight: "bold",
};

export default CodeCell;
