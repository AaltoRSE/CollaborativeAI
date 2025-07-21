import { useState } from 'react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="header-container">
      <div className='logo-container'>
        <a href="https://collaborativeai.org.aalto.fi/" style={{textDecoration: "none", color: "inherit"}}>
          <h1> 🤖🤝🧑 Collaborative AI Arena</h1>
          <h2 style={{fontWeight: "normal"}}> Benchmarking collaborative capabilities of AI in the wild </h2>
        </a>
      </div>
      <div
        className={`navbar-dropdown ${isMenuOpen ? 'open' : ''}`}
        onClick={() => setIsMenuOpen(!isMenuOpen)}
      >
        ☰
      </div>
      <nav className={`navbar ${isMenuOpen ? 'open' : ''}`}>
        <a href="https://collaborativeai.org.aalto.fi/" target="_blank">Home page</a>
        <a href="https://collaborativeai.org.aalto.fi/leaderboard" target="_blank">Leaderboard</a>
      </nav>
    </div>
  );
};

export default Header;
