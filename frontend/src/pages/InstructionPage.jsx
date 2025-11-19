import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/InstructionPage.css";

function InstructionPage() {
  const navigate = useNavigate();

  return (
    <div className="how-to-use-page">
      <header className="page-header">
          <div className="header-content">
            <button className="back-button" onClick={() => navigate("/")}>
              <svg className="back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back
            </button>
            <h1 className="logo-text">Matika</h1>
            <div className="spacer" />
          </div>
      </header>

      <main className="main-content">
        <div className="intro-section">
          <h1 className="page-title">How to Use Matika?</h1>
          <p className="page-subtitle">
            Explore all the features and learn how to make the most of the platform
          </p>
        </div>

        <div className="steps-guide">
          <div className="guide-card">
            <div className="guide-header">
              <div className="guide-icon guide-icon-calculator">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <div className="guide-content">
                <h3 className="guide-title">Step 1: Enter Your Problem</h3>
                <p className="guide-description">
                  Type your math problem into the input field. You can enter equations, 
                  algebraic expressions, or arithmetic operations. Use the top bar to add more cells – have multiple problems? Solve them simultaneously.
                </p>
                <div className="example-box">
                  <p className="example-text">
                    Example: "x^2 + 5x + 6 = 0"
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="guide-card">
            <div className="guide-header">
              <div className="guide-icon guide-icon-upload">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>
              <div className="guide-content">
                <h3 className="guide-title">Step 2: Use the Formulas</h3>
                <p className="guide-description">
                  On the right side, you'll find a column with formulas. Search by categories or names. Clicking a formula tile will automatically insert it into the active cell. 
                  Remember to type the expression you want to apply the formula to after selecting it!
                </p>
                <div className="example-box">
                  <p className="example-text">
                    Example: "!product_of_powers a^2*a^3"
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="guide-card">
            <div className="guide-header">
              <div className="guide-icon guide-icon-sparkles">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
              </div>
              <div className="guide-content">
                <h3 className="guide-title">Step 3: Get the Solution</h3>
                <p className="guide-description">
                  Want to perform a transformation? Just use /. 
                  In a few seconds, you'll receive a detailed step-by-step solution. 
                  Each step is clearly explained so you can understand the thought process. 
                </p>
                <div className="example-box">
                  <p className="example-text">
                    Example: "/+2"
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="guide-card">
            <div className="guide-header">
              <div className="guide-icon guide-icon-book">
                <svg className="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <div className="guide-content">
                <h3 className="guide-title">Step 4: Learn and Improve</h3>
                <p className="guide-description">
                  You don't just get the answer – you learn! Analyze each step, understand the logic, and apply this knowledge to future problems. This is key to mastering math.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="tips-section">
          <h2 className="tips-title">Tips for Best Results</h2>
          <div className="tips-grid">
            <div className="tip-card">
              <h4 className="tip-heading">✓ Be Careful</h4>
              <p className="tip-text">
                After pressing "Enter", your problem will be sent for solving. Check the results to make sure there are no mistakes in the input.
              </p>
            </div>
            <div className="tip-card">
              <h4 className="tip-heading">✓ Use Proper Notation</h4>
              <p className="tip-text">
                 Use standard mathematical notations (x^2, sqrt, *, itp.).
              </p>
            </div>
            <div className="tip-card">
              <h4 className="tip-heading">✓ Use Formulas</h4>
              <p className="tip-text">
              This built-in tool will help you solve expressions faster.
              </p>
            </div>
            <div className="tip-card">
              <h4 className="tip-heading">✓ Learn from Solutions</h4>
              <p className="tip-text">
                Don't just copy – understand every step of the solving process.
              </p>
            </div>
          </div>
        </div>

        <div className="final-cta">
          <h2 className="final-cta-title">Ready to Get Started?</h2>
          <p className="final-cta-text">
            Try Matika now and see how easy it is to master math!
          </p>
          <button className="cta-button" onClick={() => navigate("/user")}>
            Solve Your First Problem
          </button>
        </div>
      </main>
    </div>
  );
}

export default InstructionPage;
