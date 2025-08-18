import { useState, useEffect, useRef } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'

const ConversationDisplay = ({ isLoading, setIsLoading, floorDescription, isDisabled, messages, addMessage }) => {
  const [newComment, setNewComment] = useState("");
  const messagesRef = useRef(null);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])
  
  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let floor = "";
    let comment = "";

    // Trim the input to remove leading/trailing whitespace
    input = input.trim();
    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            floor = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }

    // console.log("Parsed: ", floor, ", ", comment)

    return { floor, comment };
}

function checkAndAddMessage(sender, text, comment, type) {
  text = (typeof text === 'string' && text.trim()) ? text : null;
  comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

  if (text === null && comment === null) {
    console.log("no message");
  } else {
    addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
  }
}

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!newComment.trim()) {
      return;
    }

    setIsLoading(true);
    checkAndAddMessage("user", null, newComment,"dialogue");

    taskService
        .submitUserInput({
          inputData: {
            floorplans: messages
          }, 
          text: newComment,
          ojective: "bedroom"
        })
        .then((returnedResponse) => {
          console.log(returnedResponse)
          let parsed = parsePoetryAndComment(returnedResponse.text)
          console.log(returnedResponse)
          console.log(parsed)
          checkAndAddMessage("ai", parsed.floor, parsed.comment,"dialogue")
          setIsLoading(false)
        })
        .catch((error) => {
          if (error.response && error.response.status === 429) {
            alert(error.response.data.error);
          } else {
            console.log(error);
          }
          setIsLoading(false)
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
