import React, { useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { syntaxHighlighting } from "@codemirror/language";
import { oneDark } from "@codemirror/theme-one-dark";
import { myLang, myLangHighlight } from "../highlighting";
import { EditorView, placeholder as cmPlaceholder } from "@codemirror/view"; 

const CodeEditor = ({ value, onChange, onEnter }) => {
  const editorRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { 
      if (onEnter) onEnter();
    }
  };

  return (
    <div
      ref={editorRef}
      onKeyDown={handleKeyDown}
      style={{ outline: "none" }} 
    >
      <CodeMirror
        value={value}
        height="700px"
        width="700px"
        theme={oneDark}
        extensions={[myLang, syntaxHighlighting(myLangHighlight), EditorView.lineWrapping, cmPlaceholder("Type your math problem")]}
        onChange={onChange}
      />
    </div>
  );
};

export default CodeEditor;
