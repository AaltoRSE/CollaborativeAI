import { useState, useEffect, useRef } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'

const ConversationDisplay = ({ isLoading, setIsLoading, recipeDescription, isDisabled, messages, addMessage }) => {
  const [newComment, setNewComment] = useState("");
  const messagesRef = useRef(null);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!newComment.trim()) {
      return;
    }
    setIsLoading(true);
    addMessage({ sender: "user", recipe: "", comment: newComment}); 

    taskService
        .submitUserInput({
          inputData: {
            comment: true,
            recipes: messages
          }, 
          text: newComment, 
          ojective: recipeDescription
        })
        .then((returnedResponse) => {
          let parsed = JSON.parse(returnedResponse.text)
          addMessage({ sender: "ai", recipe: parsed.recipe, comment: parsed.comment})
          setIsLoading(false)
        })
        .catch((error) => {
          console.log(error)
        });
    setNewComment("");
  };

  return (
    <div className="chat-space-wrapper">
      <h2>Conversation</h2>
      <div className="chat-space">
        <div className="messages" ref={messagesRef}>
          {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          }
        </div>
        {isLoading && <div>Waiting for response...</div>} 
        <div className="form-wrapper">
          <form onSubmit={handleSubmit} className="input-form">
            <input 
              value={newComment}
              disabled={!isDisabled || isLoading}
              onChange={(event) => setNewComment(event.target.value)} 
              placeholder="Send a message to the AI" 
            />
            <button type="submit" 
              disabled={!isDisabled || isLoading}
              onClick={handleSubmit}> 
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
