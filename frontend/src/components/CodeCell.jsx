import React, { useState, useEffect, useRef } from "react";
import CodeEditor from "./CodeEditor";
import { sendText } from "../services/api";

const CodeCell = ({ cellId, content, onChange, onRemove, isRemovable, onFocus }) => {
  const [outputs, setOutputs] = useState([]);
  const [running, setRunning] = useState(false);

  const resultRef = useRef(null);
  useEffect(() =>{
    if (resultRef.current) {
      resultRef.current.scrollTop = resultRef.current.scrollHeight;
    }
  },[outputs]); 
  const handleRun = async () => {
    if (!content.trim()) return;   
    setRunning(true);
    const lines = content.split("\n").filter((l) => l.trim() !== "");
    let timeout;

    try { 
      const res = await Promise.race([
        sendText(lines.join("\n")),
        new Promise((_, reject) => {
          timeout = setTimeout(() => reject(new Error("Timeout: no response in 3s")), 3000);
        }),
      ]);

      const results = res.steps.map((e, i) => ({ line: e, output: res.steps[i] }));
      setOutputs(results);
    } catch (err) {
        console.error("Cannot connect to backend: ", err);
        setOutputs([{line: "Error", output: err.message}]);
    } finally {
      clearTimeout(timeout);
      setRunning(false);
    }
  };

  useEffect(() => {
    const handler = (e) => {
      if (e.detail.cellId === cellId) onChange(cellId, content + e.detail.latex);
    };
    window.addEventListener("insertFormula", handler);
    return () => window.removeEventListener("insertFormula", handler);
  }, [cellId, content, onChange]);

  useEffect(() => {
    const handleGlobalRun = () => handleRun();
    window.addEventListener("runAllCells", handleGlobalRun);
    return () => window.removeEventListener("runAllCells", handleGlobalRun);
  }, [content]);

  return (
    <div className="codecell" style={{ position: "relative", marginBottom: "20px" }}>
      {isRemovable && (
        <button onClick={() => onRemove && onRemove(cellId)} className="remove-cell-btn" title="Remove cell">
          <svg className="remove-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}

      <div onClick={() => onFocus && onFocus()} style={{ cursor: "text" }}>
        <CodeEditor value={content} onChange={(newCode) => onChange(cellId, newCode)} onEnter={handleRun} />
      </div>

      <div className="codecell-buttons">
        <button onClick={handleRun} className="icon-btn" title="Run">
          <svg className="solve-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          Run
          {running ? " Running..." : ""}
        </button>
      </div>

      {outputs.length > 0 && (
      <div className="results-wrapper">
        <div className="results" ref={(resultRef)}>
          {outputs.map((item, i) => (
            <div key={i} className="result-line">
              <span className="result-step">{item.line}</span>
              <span className="result-value">{item.output}</span>
            </div>
          ))}
        </div>
      </div>
      )}
    </div>
  );
};

export default CodeCell;