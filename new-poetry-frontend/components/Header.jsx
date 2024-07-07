const Header = () => {
  return (
    <div className="header-container">
      <div className="header-content">
        <h1 style={{margin: 0}}> 🤖🤝🧑 Collaborative AI Arena </h1>
        <h2 style={{fontWeight: 'normal',margin: 0}}> Benchmarking collaborative capabilities of AI in the wild </h2>
      </div>
      <nav className="navbar">
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Task</a></li>
          <li><a href="#">About Us</a></li>
        </ul>
      </nav>
    </div>
  );
};

export default Header;
