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

    var res;

    try { 
        res = await sendText(lines.join("\n"));
      } catch (err) {
        console.error("Cannot connect to backend:", err);
    }

    console.log("Response:", res.final);
    const results = lines.map(function(e, i) {
          return { line: e, output: res.steps[i] };
    });


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
