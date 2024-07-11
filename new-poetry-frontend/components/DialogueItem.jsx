const DialogueItem = ({ message }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";
  return (
    <>
      <div className={`dialogue-message ${messageClass}`}>
        {message.text}
        <button type="submit" className="dialogue-button"> Edit </button>
      </div>
    </>
  );
};

export default DialogueItem;
