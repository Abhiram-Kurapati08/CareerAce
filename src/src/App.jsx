import React from 'react';
import './App.css';
import ResponsivePage from './components/ResponsivePage';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  const handleNavigation = () => {
    navigate('/responsive');
  };

  const goToHome = () => {
    navigate('/');
  };

  return (
    <div className="app">
      {/* Navigation Bar */}
      <nav className="navbar">
        <button className='logo-button' onClick={goToHome}>
          <h1 className="logo">CareerAce</h1>
        </button>
        <div className="navlinks">
          <a href="#get-app" className="navLinkStyle">Get App</a>
          <a href="#features" className="navLinkStyle">Features</a>
          <a href="#about" className="navLinkStyle">About</a>
          <a href="#faq" className="navLinkStyle">F.A.Q.</a>
          <a href="#signin" className="navLinkStyle">Sign In</a>
          <a href="#signup" className="signup-button">Sign Up</a>
        </div>
      </nav>

      <div className="heading">
        <h2>Ready to become a Space Cowboy</h2>
      </div>

      <div className="content">
        <p>Discover a personalized career roadmap tailored to your skills, aspirations, and the dynamic job market.</p>
        
        <button className="chat-button" onClick={handleNavigation}>
          Chat Now
        </button>

        <a 
          href="https://insigh.to/b/careerace" 
          className="feedback-button" 
        >
          Help Us Level Up!!
        </a>
      </div>

      <Footer />
    </div>
  );
};

const Footer = () => {
  return (
    <footer className="footer">
      <div>
        <h3>
          About CareerAce</h3>
          <p>
          CareerAce is a platform designed for students who are seeking jobs, 
            unsure of which career path to take, or exploring various job opportunities. 

          </p>
        <p>© {new Date().getFullYear()} CareerAce. All Rights Reserved.</p>
      </div>
    </footer>
  );
};

const App = () => {
  return (
   
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/responsive" element={<ResponsivePage />} />
      </Routes>
   
  );
};

export default App;
