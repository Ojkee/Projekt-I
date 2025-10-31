import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/InstructionPage.css";

function InstructionPage() {
  const navigate = useNavigate();

  return (
    <div className="instruction-container">
      <h1 className="instruction-title">Witaj w aplikacji!</h1>

      <p className="instruction-intro">
        Ta aplikacja pozwala tworzyć, uruchamiać i eksperymentować z komórkami kodu matematycznego. 
        Możesz korzystać z gotowych wzorów lub pisać własne równania i skrypty.
      </p>

      <div className="instruction-section">
        <h2>Tworzenie komórek</h2>
        <p>
          Każda komórka to niezależny blok kodu, który możesz edytować i uruchamiać. 
          Aby dodać nową komórkę, kliknij <strong>"Dodaj komórkę"</strong> w górnym panelu. 
          Aby usunąć komórkę, kliknij ikonę <span className="icon">X</span> w prawym górnym rogu komórki.
        </p>
      </div>

      <div className="instruction-section">
        <h2>Uruchamianie kodu</h2>
        <p>
          Aby wykonać kod w komórce, kliknij ikonę <span className="icon">▶</span> w komórce. 
          Możesz też uruchomić wszystkie komórki naraz, klikając <strong>"Uruchom wszystkie"</strong> w panelu górnym.
        </p>
      </div>

      <div className="instruction-section">
        <h2>Formuły i wzory</h2>
        <p>
          W prawej kolumnie znajdziesz gotowe wzory matematyczne. 
          Kliknięcie wzoru automatycznie wstawia go do aktywnej komórki. 
          Możesz wyszukiwać wzory po nazwie lub kategorii.
        </p>
      </div>

      <div className="instruction-section">
        <h2>Wyniki i podgląd</h2>
        <p>
          Po uruchomieniu kodu w komórce wyniki zostaną wyświetlone pod komórką. 
          Każdy krok lub wynik końcowy jest wyraźnie oznaczony, dzięki czemu łatwo śledzić obliczenia.
        </p>
      </div>

      <button className="instruction-btn" onClick={() => navigate("/")}>
        Przejdź do strony głównej
      </button>
    </div>
  );
}

export default InstructionPage;
