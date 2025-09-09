const Header = () => {
  return (
    <div className="header-container">
      <div className='logo-container'>
        <a href="https://collaborativeai.org.aalto.fi/" style={{textDecoration: "none", color: "inherit"}}>
          <h1> 🤖🤝🧑 Collaborative AI Arena</h1>
          <h2 style={{fontWeight: "normal"}}> Benchmarking collaborative capabilities of AI in the wild </h2>
        </a>
      </div>
      <nav className="navbar">
        <a href="https://collaborativeai.org.aalto.fi/" target="_blank">Home page</a>
        <a href="https://collaborativeai.org.aalto.fi/leaderboard" target="_blank">Leaderboard</a>
      </nav>
    </div>
  );
};

export default Header;
