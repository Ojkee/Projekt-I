import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  const handleClick = async () => {
    try {
      const res = await fetch("http://localhost:8080/hello", { method: "POST" });
      const data = await res.json();
      setMessage(data.message);
    } catch (err) {
      setMessage("Error connecting to backend");
      console.error(err);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <button onClick={handleClick}>Say Hello</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
