const ConversationalItem = ({ message }) => {
  const messageClass = message.sender === 'user' ? 'user-message' : 'ai-message';
  return (
    <div className={`message ${messageClass}`}>
      {message.text}
    </div>
  );
};

export default ConversationalItem;
