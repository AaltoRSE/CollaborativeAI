const ConversationalItem = ({ message }) => {
  const messageClass = message.sender === "user" ? "user-message" : "ai-message";
  const avatarClass = message.sender === "user" ? "avatar-user" : "avatar-ai";
  const avatarText = message.sender === "user" ? "You" : "AI";

  return (
    <>
      <div className={`message ${messageClass}`}>
        {message.sender === "user" ? (
          <>
            {message.text}
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
          </>
        ) : (
          <>
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
            <b>New line: </b> {message.text}
          </>
        )}
      </div>
    </>
    
  );
};

export default ConversationalItem;
