import React from "react";
import { EditorView } from "@codemirror/view";
import { syntaxHighlighting } from "@codemirror/language";
import CodeMirror from "@uiw/react-codemirror";
import { oneDark } from "@codemirror/theme-one-dark";
import { myLang, myLangHighlight } from "../highlighting.ts";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
}

const CodeEditor: React.FC<CodeEditorProps> = ({ value, onChange }) => {
  return (
    <CodeMirror
      value={value}
      height="200px"
      theme={oneDark}
      extensions={[myLang, syntaxHighlighting(myLangHighlight), EditorView.lineWrapping]}
      onChange={onChange}
    />
  );
};

export default CodeEditor;
