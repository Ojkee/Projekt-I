import React, { useState, useEffect, useRef } from "react";
import CodeEditor from "./CodeEditor";
import { sendText } from "../services/api";

const CodeCell = ({ cellId, content, onChange, onRemove, isRemovable, onFocus }) => {
  const [outputs, setOutputs] = useState([]);
  const [running, setRunning] = useState(false);
  const insertRef = useRef(null);
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

    const result = (res.steps || []).map((step, i) => ({
      line: lines[i],
      output: step
    }));

    setOutputs(result);
  } catch (err) {
    console.error("Cannot connect to backend: ", err);
    setOutputs([{ line: "Error", output: err.message }]);
  } finally {
    clearTimeout(timeout);
    setRunning(false);
  }
};

  useEffect(() => {
    const handler = (e) => {
      if (e.detail.cellId === cellId && insertRef.current) {
        insertRef.current(e.detail.f_name);
      }
    };
    window.addEventListener("insertFormula", handler);
    return () => window.removeEventListener("insertFormula", handler);
  }, [cellId, content]);

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
        <CodeEditor value={content} onChange={(newCode) => onChange(cellId, newCode)} onEnter={handleRun} onExposeInsert={(fn) => (insertRef.current = fn)} />
      </div>

      <div className="codecell-buttons">
        <button onClick={handleRun} className="icon-btn" title="Run">
          <svg className="solve-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          Run
          {running ? " Running..." : ""}
        </button>
        <button className="icon-btn" title="Simplify" onClick={() =>
          window.dispatchEvent(
            new CustomEvent("insertFormula", {
              detail:{cellId, f_name: "!simplify"}
            })
          )
        }>
          Simplify
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