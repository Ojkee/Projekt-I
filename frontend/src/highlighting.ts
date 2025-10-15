import { StreamLanguage } from "@codemirror/language";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { tags } from "@lezer/highlight";

export const myLang = StreamLanguage.define({
  token: (stream) => {
    if (stream.eatSpace()) return null;

    //if (stream.match("//")) {stream.skipToEnd();return "comment";}

    if (stream.match(/^[0-9]+/)) return "number";

    if (stream.match(/^(!formula)\b/)) return "keyword";

    if (stream.match(/^[a-zA-Z_]\w*/)) return "variableName";

    if (stream.match(/^[+\-*/=<>!]+/)) return "operator";

    if (stream.match(/^[()[\]{}]/)) return "bracket";

    stream.next();
    return null;
  },
});

// Kolorowanie składni
export const myLangHighlight = HighlightStyle.define([
  { tag: tags.keyword, color: "#ff6188", fontWeight: "bold" },
  { tag: tags.variableName, color: "#ffd866" },
  { tag: tags.comment, color: "#727072", fontStyle: "italic" },
  { tag: tags.number, color: "#ab9df2" },
  { tag: tags.operator, color: "#78dce8" },
  { tag: tags.bracket, color: "#fc9867" },
]);
