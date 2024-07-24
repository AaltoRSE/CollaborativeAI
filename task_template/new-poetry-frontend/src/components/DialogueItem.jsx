const DialogueItem = ({ message }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  let newLine = ""
  const poemLine = message.text.match(/\[(.*?)\]/);
  if (poemLine) {
    newLine = poemLine[1];
  } else {
    newLine = message.text
  }

  return (
    <>
      <div className={`dialogue-message ${messageClass}`}>
        {newLine}
        {/* <button type="submit" className="dialogue-button"> Edit </button> */}
      </div>
    </>
  );
};

export default DialogueItem;
