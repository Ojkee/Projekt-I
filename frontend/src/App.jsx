import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import UserPage from "./pages/UserPage";
import InstructionPage from "./pages/InstructionPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/user" element={<UserPage />} />
        <Route path="/how-to-use" element={<InstructionPage />} />
      </Routes>
    </Router>
  );
}

export default App;
