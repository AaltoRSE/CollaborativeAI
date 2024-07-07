const Dialogue = ({ messages }) => {
  return (
    <div className="dialogue">
      {messages.map((msg, index) => (
        <div key={index} className={`message poem-message`}> {msg.text} </div>
      ))}
    </div>
  );
};

export default Dialogue;
