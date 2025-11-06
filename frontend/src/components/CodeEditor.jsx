import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { EditorView } from "@codemirror/view";
import { syntaxHighlighting } from "@codemirror/language";
import { oneDark } from "@codemirror/theme-one-dark";
import { myLang, myLangHighlight } from "../highlighting";

const CodeEditor = ({ value, onChange }) => {
  return (
    <CodeMirror
      value={value}
      height="700px"
      width="700px"  
      theme={oneDark}
      extensions={[myLang, syntaxHighlighting(myLangHighlight), EditorView.lineWrapping]}
      onChange={onChange}
    />
  );
};

export default CodeEditor;
