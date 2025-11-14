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
    const results = res.steps.map(function(e, i) {
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
          className="remove-cell-btn"
          title="Remove cell"
        >
          <svg className="remove-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}

      <div onClick={() => onFocus && onFocus()} style={{ cursor: "text" }}>
        <CodeEditor value={code} onChange={setCode} onEnter={handleRun} />
      </div>

      <div className="codecell-buttons">
        <button onClick={handleRun} className="icon-btn" title="Run">
          <svg className="solve-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          Solve
          {running ? " Running..." : ""}
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


export default CodeCell;
