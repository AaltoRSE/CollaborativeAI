const DialogueItem = ({ message, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  let newLine = ""
  const poemLine = message.text.match(/\[(.*?)\]/);
  if (poemLine) {
    newLine = poemLine[1];
  } else {
    newLine = message.text
  }
  // The <br /> here is to basically get a line break between the user and AI dialogue. Can add more or just remove it based on your task 
  return (
    <>
      <div className={`${style} ${messageClass}`}>
        {newLine} <br />
        {/* <button type="submit" className="dialogue-button"> Edit </button> */}
      </div>
    </>
  );
};

export default DialogueItem;
