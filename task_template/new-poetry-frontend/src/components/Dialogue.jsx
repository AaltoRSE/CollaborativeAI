import DialogueItem from "./DialogueItem";
import { dialogueType } from "../utils/config";

const Dialogue = ({ messages }) => {
  let style = "none";
  if (dialogueType === "paragraph") {
    style = "dialogue-paragraph";
  } else {
    style = "dialogue-poem";
  }

  return (
    <div className="dialogue-wrapper">
      <h2>Your joint poem</h2>
      <div className="dialogue">
        {messages.map((msg, index) => (
          msg.type=="dialogue" && <DialogueItem key={index} message={msg} style={style}/>
        ))}
      </div>
    </div>
  );
};

export default Dialogue;
