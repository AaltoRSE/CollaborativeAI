import DialogueItem from "./DialogueItem";
import { dialogueType } from "../utils/config";

const Dialogue = ({ messages, setMessages }) => {
  let style = "none";
  if (dialogueType === "paragraph") {
    style = "dialogue-paragraph";
  } else {
    style = "dialogue-poem";
  }

  const handleEditMessage = (index, newMessage) => {
    setMessages(messages.map((message, idx) => idx !== index ? message : { ...message, text: newMessage }))
  };

  return (
    <div className="dialogue-wrapper">
      <h2>Your joint poem</h2>
      <div className="dialogue">
        {messages.map((msg, index) => (
          msg.type=="dialogue" && 
          <DialogueItem 
            key={index}
            idx={index}
            message={msg} 
            handleEditMessage={handleEditMessage} 
            style={style}
          />
        ))}
      </div>
    </div>
  );
};

export default Dialogue;
