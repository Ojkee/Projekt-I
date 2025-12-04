import React, { useEffect, useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { syntaxHighlighting } from "@codemirror/language";
import { oneDark } from "@codemirror/theme-one-dark";
import { myLang, myLangHighlight } from "../highlighting";
import { EditorView, placeholder as cmPlaceholder } from "@codemirror/view"; 

const CodeEditor = ({ value, onChange, onEnter, onExposeInsert }) => {
  const viewRef = useRef(null);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { 
      if (onEnter) onEnter();
    }
  };

  const insertAtCursor = (text) => {
    const view = viewRef.current;
    if (!view) return;

    const {from, to} = view.state.selection.main;
    view.dispatch({
      changes: {from,to, insert: text},
      selection: {anchor: from + text.length}
    });

    view.focus();
  }

  useEffect(() => {
    if (onExposeInsert) onExposeInsert(insertAtCursor);
  }, [onExposeInsert]);

  return (
    <div
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
        onCreateEditor={(view) => (viewRef.current = view)}
      />
    </div>
  );
};

export default CodeEditor;
