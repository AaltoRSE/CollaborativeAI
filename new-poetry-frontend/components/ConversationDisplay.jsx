import { useState } from 'react';
import ConversationItem from './ConversationItem';

const ConversationDisplay = ({ messages, addMessage }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      addMessage({ sender: 'user', text: input });
      setInput('');
      setTimeout(() => addMessage({ sender: 'ai', text: 'AI response placeholder' }), 1000);
    }
  };

  return (
    <div className="chat-space">
      <div className="messages">
        {messages.map((msg, index) => (
          <ConversationItem key={index} message={msg} /> 
        ))}
      </div>
      <form onSubmit={handleSubmit} className="input-form">
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          placeholder="Type a message" 
        />
        <button type="submit" style={{"background-color": "green"}}> Submit </button>
        <button type="submit" style={{"background-color": "green"}}> Finish </button>
      </form>
    </div>
  );
};

export default ConversationDisplay;
