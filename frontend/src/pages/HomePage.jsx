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
                Solve problems with{" "}
                <span className="hero-title-highlight">Matika</span>
              </h1>
              <p className="hero-description">
                Matika is a tool that will help you with math challenges. Try it and see how simple it can be.
              </p>
              <div className="hero-buttons">
                <button 
                  className="btn btn-primary"
                  onClick={() => navigate("/user")}
                >
                  Get Started
                </button>
                <button 
                  className="btn btn-secondary"
                  onClick={() => navigate("/how-to-use")}
                >
                  How to Use?
                </button>
              </div>
            </div>
            <div className="hero-image-wrapper">
              <div className="hero-image-glow" />
              <img 
                src={heroImage} 
                alt="Matika" 
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
              Why Matika?
            </h2>
            <p className="section-description">
              Everything you need to succed in math - all in one place
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
                <div className="feature-icon feature-icon-primary">
                  <svg
                    className="icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="white"
                  >
                    <path
                      d="M4 6h16M4 12h16M4 18h16"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </div>
              <h3 className="feature-title">Step-by-Step Solutions</h3>
              <p className="feature-description">
                Get detailed explanations for every problem. Understand the "why" behind each step, not just the answer.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon feature-icon-secondary">
                <svg
                  className="icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="white"
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
              <h3 className="feature-title">Instant Help</h3>
              <p className="feature-description">
                Receive instant, easy-to-understand answers whenever you need them.
              </p>
            </div>
            <div className="feature-card">
              <div className="feature-icon feature-icon-accent">
                <svg
                  className="icon"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="white"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="6" cy="6" r="3" />
                  <circle cx="18" cy="6" r="3" />
                  <circle cx="6" cy="18" r="3" />
                  <circle cx="18" cy="18" r="3" />
                  <path d="M9 6h6M6 9v6M18 9v6M9 18h6" />
                </svg>
              </div>
              <h3 className="feature-title">Multitasking</h3>
              <p className="feature-description">
                Have multiple problems to solve? You can solve them all at once and see results simultaneously.
              </p>
            </div>
          </div>          
        </div>
      </section>

      <section className="steps-section">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">
              Get result in 3 simple steps
            </h2>
          </div>
          
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3 className="step-title">Enter your problem</h3>
                <p className="step-description">Type an expression, equation, or use ready-made formulas</p>
              </div>
              <svg className="step-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <div className="step-item">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3 className="step-title">Get instant solutions</h3>
                <p className="step-description">Receive detailed step-by-step explanations in just a few seconds</p>
              </div>
              <svg className="step-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>

            <div className="step-item">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3 className="step-title">Learn and improve</h3>
                <p className="step-description">Master concepts and understand the topic thoroughly</p>
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
            Ready to ace your math?
          </h2>
          <p className="cta-description">
            Enter a problem and we'll help you
          </p>
          <button className="btn btn-cta" onClick={() => navigate("/user")}>
            Start for Free
          </button>
        </div>
      </section>
    </div>
  );
};

export default HomePage;


