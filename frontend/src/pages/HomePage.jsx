import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/HomePage.css";
import heroImage from "../assets/hero-math.jpg";

function HomePage() {
  const navigate = useNavigate();

  function goToUserPage() {
    navigate("/user");
  }

    function goToInstructionPage() {
    navigate("/how-to-use");
  }

  return (
    <div className="page-container">
      <section className="hero-section">
        <div className="container">
          <div className="hero-grid">
            <div className="hero-content">
              <h1 className="hero-title">
                Rozwiązuj zadania z{" "}
                <span className="hero-title-highlight">Matiką</span>
              </h1>
              <p className="hero-description">
                Matika to narzędzie, które pomoże Ci w zagadnieniach matematycznych. Przetestuj i zobacz jakie to proste.
              </p>
              <div className="hero-buttons">
                <button 
                  className="btn btn-primary"
                  onClick={() => navigate("/user")}
                >
                  Zacznij teraz
                </button>
                <button 
                  className="btn btn-secondary"
                  onClick={() => navigate("/how-to-use")}
                >
                  Jak używać?
                </button>
              </div>
            </div>
            <div className="hero-image-wrapper">
              <div className="hero-image-glow" />
              <img 
                src={heroImage} 
                alt="Uczniowie uczący się matematyki z Matiką" 
                className="hero-image"
              />
            </div>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">
              Dlaczego Matika?
            </h2>
            <p className="section-description">
              Wszystko czego potrzebujesz, aby osiągnąć sukces w matematyce - w jednym miejscu
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
                <div className="feature-icon feature-icon-primary">
                  <svg
                    className="icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                  >
                    <path
                      d="M4 6h16M4 12h16M4 18h16"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              <h3 className="feature-title">Rozwiązania krok po kroku</h3>
              <p className="feature-description">
                Otrzymaj szczegółowe wyjaśnienia dla każdego problemu. Zrozum "dlaczego" za każdym krokiem, 
                nie tylko odpowiedź.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon feature-icon-secondary">
                <svg
                  className="icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <circle cx="12" cy="12" r="10" strokeWidth="2" />
                  <path
                    d="M12 8v4l3 3"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </div>
              <h3 className="feature-title">Wszechstronne tematy</h3>
              <p className="feature-description">
                Od algebry po rachunek różniczkowy, trygonometrię po statystykę. Pomożemy Ci w każdym temacie jaki masz w szkole/liceum.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="steps-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">
              Otrzymaj pomoc w 3 prostych krokach
            </h2>
          </div>
          
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3 className="step-title">Wprowadź swoje zadanie</h3>
                <p className="step-description">Wpisz wyrażenie, równanie lub skorzystaj z gotowych wzorów</p>
              </div>
              <svg className="step-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <div className="step-item">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3 className="step-title">Otrzymaj natychmiastowe rozwiązania</h3>
                <p className="step-description">Otrzymaj szczegółowe wyjaśnienia krok po kroku w ciągu kilku sekund</p>
              </div>
              <svg className="step-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <div className="step-item">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3 className="step-title">Ucz się i doskonal</h3>
                <p className="step-description">Opanuj koncepcje i zrozum dane zagadnienie</p>
              </div>
              <svg className="step-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container cta-content">
          <h2 className="cta-title">
            Gotowy, aby zdobyć piątkę z matematyki?
          </h2>
          <p className="cta-description">
            Wpisz przykład i Ci pomożemy
          </p>
          <button className="btn btn-cta" onClick={() => navigate("/user")}>
            Rozpocznij za darmo
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;


