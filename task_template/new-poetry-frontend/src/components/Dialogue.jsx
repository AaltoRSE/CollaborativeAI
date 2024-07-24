import DialogueItem from "./DialogueItem";

const Dialogue = ({ messages }) => {
  return (
    <div className="dialogue-wrapper">
      <h2>Your joint poem</h2>
      <div className="dialogue">
        {messages.map((msg, index) => (
          msg.type=="dialogue" && <DialogueItem key={index} message={msg} /> 
        ))}
      </div>
    </div>
  );
};

export default Dialogue;
