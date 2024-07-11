const Header = () => {
  return (
    <div className="header-container">
      <div className="header-content">
        <h1 style={{
          "margin": 0
        }}> 🤖🤝🧑 Collaborative AI Arena </h1>
        <h2 style={{
          "font-weight": "normal", 
          "margin": 0
        }}> Benchmarking collaborative capabilities of AI in the wild </h2>
      </div>
      <nav className="navbar">
        <a href="#">Home</a>
        <a href="#">Task</a>
        <a href="#">About Us</a>
      </nav>
    </div>
  );
};

export default Header;
