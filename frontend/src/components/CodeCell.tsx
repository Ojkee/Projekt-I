import React, { useState } from "react";
import CodeEditor from "./CodeEditor";
import { LucidePlus, LucidePlay, LucideTrash } from "lucide-react";
import { sendText } from "../services/api"; // <-- import funkcji

interface CodeCellProps {
  cellId: number;
  onAdd?: (afterId: number) => void;
  onRemove?: (id: number) => void;
}

const CodeCell: React.FC<CodeCellProps> = ({ cellId, onAdd, onRemove }) => {
  const [code, setCode] = useState<string>(""); // wejściowy kod
  const [lines, setLines] = useState<string[]>([]); // linie transformacji
  const [outputs, setOutputs] = useState<string[]>([]);
  const [finalOutput, setFinalOutput] = useState<string>("");
  const [running, setRunning] = useState<boolean>(false);

const handleRun = async () => {
  if (!code) return;
  setRunning(true);

  try {
    const result = await sendText(code); 

    const stepsArray: string[] = Array.isArray(result.steps) ? result.steps : [];

    const finalStr = typeof result.final === "string" ? result.final : "";

    setLines(stepsArray.map((_, idx) => `Step ${idx + 1}:`));
    setOutputs(stepsArray);
    setFinalOutput(finalStr);

  } catch (err) {
    console.error("Error running cell:", err);
    setOutputs([]);
    setFinalOutput("Error");
  } finally {
    setRunning(false);
  }
};
  return (
    <div
      style={{
        marginBottom: "20px",
        background: "rgba(255,255,255,0.05)",
        borderRadius: "12px",
        padding: "10px",
        backdropFilter: "blur(10px)",
        border: "1px solid rgba(255,255,255,0.1)",
      }}
    >
      {/* linia wejściowa */}
      <div style={{ marginBottom: "8px" }}>
        <CodeEditor value={code} onChange={setCode} />
      </div>

      {/* przyciski pod linią wejściową */}
      <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
        {onAdd && (
          <button onClick={() => onAdd(cellId)} style={iconButtonStyle} title="Add cell">
            <LucidePlus size={16} />
          </button>
        )}
        <button onClick={handleRun} style={iconButtonStyle} title="Run cell">
          <LucidePlay size={16} />
          {running && " ..."}
        </button>
        {onRemove && (
          <button onClick={() => onRemove(cellId)} style={iconButtonStyle} title="Remove cell">
            <LucideTrash size={16} />
          </button>
        )}
      </div>

      {/* Wyniki transformacji */}
      {lines.map((line, index) => (
        <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: "4px" }}>
          <div style={{ flex: 1, marginRight: "8px", fontFamily: "monospace", color: "#fff" }}>
            {line}
          </div>
          <div
            style={{
              width: "200px",
              color: "rgba(255,255,255,0.5)",
              background: "rgba(0,0,0,0.1)",
              padding: "4px 8px",
              borderRadius: "6px",
              fontFamily: "monospace",
            }}
          >
            {outputs[index]}
          </div>
        </div>
      ))}

      {finalOutput && (
        <div
          style={{
            marginTop: "12px",
            padding: "8px",
            background: "rgba(255,255,255,0.1)",
            borderRadius: "6px",
            color: "#fff",
            fontFamily: "monospace",
          }}
        >
          <strong>Final function:</strong> {finalOutput}
        </div>
      )}
    </div>
  );
};

const iconButtonStyle: React.CSSProperties = {
  border: "none",
  background: "rgba(255,255,255,0.1)",
  color: "#fff",
  borderRadius: "6px",
  padding: "4px 8px",
  cursor: "pointer",
  transition: "background 0.2s",
};

export default CodeCell;
