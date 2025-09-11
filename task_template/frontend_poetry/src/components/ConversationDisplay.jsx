import { useState, useEffect, useRef } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'
import { lengthLimit } from '../utils/config';

const ConversationDisplay = ({ isLoading, setIsLoading, theme, isDisabled, messages, addMessage }) => {
  // const [newMessage, setNewMessage] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);

  const messagesRef = useRef(null);

  //Check if the length of the text has reached the line limit yet
  useEffect(() => {
    setIsLengthReached(messages.filter(msg => msg.text !== "" && msg.text !== null).length === lengthLimit)
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])
  
  const parsePoetryAndComment = (input) => {
    let poetryLine = "";
    let comment = "";
    input = input.trim();

    if (input.includes('[')) {
      let startBracketIndex = input.indexOf('[');
      let endBracketIndex = input.indexOf(']');
      
      if (startBracketIndex !== -1 && endBracketIndex !== -1) {
        poetryLine = input.substring(startBracketIndex + 1, endBracketIndex).trim();
        let commentBeforeBracket = input.substring(0, startBracketIndex).trim();
        let commentAfterBracket = input.substring(endBracketIndex + 1).trim();

        if (commentBeforeBracket && commentAfterBracket) {
          comment = `${commentBeforeBracket} ${commentAfterBracket}`.trim();
        } else {
          comment = commentBeforeBracket || commentAfterBracket;
        }
      } else {
        comment = input
      }
    } else {
      comment = input
    }
    
    return { poetryLine, comment };
  }

  const checkAndAddMessage = (sender, text, comment, type) => {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!newComment.trim()) {
      return;
    }
    setIsLoading(true);
    checkAndAddMessage("user", null, newComment,"dialogue");   

    if (isLengthReached) {
      newComment += " The poem is finished. Do NOT add a new poetry line.";
    }

    taskService
        .submitUserInput({
          inputData: { 
            comment: true,
            poem: messages
          }, 
          text: newComment, 
          ojective: theme
        })
        .then((returnedResponse) => {
          let parsed = parsePoetryAndComment(returnedResponse.text)
          checkAndAddMessage("ai", parsed.poetryLine, parsed.comment,"dialogue")
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
      <h2>Discussion with AI</h2>
      <div className="chat-space">
        <div className="messages" ref={messagesRef}>
          {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          }
          {isLoading && messages.length == 0 && <div style={{margin: "auto"}}>Waiting for response...</div>} 
        </div>
        {isLoading && messages.length != 0 && <div>Waiting for response...</div>} 
        {isLengthReached && 
        <span 
          style={{
            "color" : "#FF0000"
          }}>
          The poem reached the length limit. Please click "Finish" to rate it
        </span>
        }
        <div className="form-wrapper">
          <form onSubmit={handleSubmit} className="input-form">
            <input 
              value={newComment}
              disabled={isLengthReached || !isDisabled || isLoading}
              onChange={(event) => setNewComment(event.target.value)} 
              placeholder="Send a message to the AI" 
            />
            <button type="submit" 
              disabled={isLengthReached || !isDisabled || isLoading}
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
