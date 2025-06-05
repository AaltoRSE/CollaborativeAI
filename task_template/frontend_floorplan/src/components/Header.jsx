const Header = () => {
  return (
    <div className="header-container">
      <div className="header-content">
        <h1> 🤖🤝🧑 Collaborative AI Arena</h1>
        <h2 style={{fontWeight: "normal"}}> Benchmarking collaborative capabilities of AI in the wild </h2>
      </div>
      <nav className="navbar">
        <a href="https://collaborativeai.org.aalto.fi/" target="_blank">Home page</a>
        <a href="https://collaborativeai.org.aalto.fi/leaderboard" target="_blank">Leaderboard</a>
      </nav>
    </div>
  );
};

export default Header;
