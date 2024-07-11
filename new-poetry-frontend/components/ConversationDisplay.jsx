import { useState } from "react";
import ConversationItem from "./ConversationItem";

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  const [newLine, setNewLine] = useState("");
  const [AIMessage, setAIMessage] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (newLine.trim()) {
      addMessage({ sender: "user", text: newLine });
      setNewLine("");
      setAIMessage("");
      setTimeout(() => addMessage({ sender: "ai", text: "AI response placeholder",  }), 1000);
    }
  };

  const toggleFinishButton = () => {
    toggleFinish();
    setIsFinishClicked(!isFinishClicked);
  }

  return (
    <div className="chat-space-wrapper">
      <h2>Discussion with AI</h2>
      <div className="chat-space">
        <div className="messages">
          {messages.map((msg, index) => (
            <ConversationItem key={index} message={msg} /> 
          ))}
        </div>
        <form onSubmit={handleSubmit} className="form-wrapper">
          <div className="input-form">
            <input 
              type="text" 
              value={AIMessage} 
              onChange={(e) => setAIMessage(e.target.value)} 
              placeholder="Send a message to the AI" 
            />
            <input 
              type="text" 
              value={newLine} 
              onChange={(e) => setNewLine(e.target.value)} 
              placeholder="Add a line to the poem" 
            />
          </div>
          <div className="button-group">
            <button type="submit" 
              style={{
                "background-color": "#4caf50"
              }}> 
              Submit 
            </button>
            <button type="submit" className="finish-button" 
              style={{
                "background-color": isFinishClicked ? "#f44336" : "#6eb4ff",
                "cursor": isFinishClicked ? "not-allowed" : "pointer"
              }}
              onClick={toggleFinishButton}> 
              {isFinishClicked ? "Cancel" : "Finish"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ConversationDisplay;
