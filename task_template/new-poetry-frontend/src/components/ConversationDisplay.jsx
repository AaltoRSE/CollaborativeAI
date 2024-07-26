import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'
import { lengthLimit } from '../utils/config';

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  // const [newMessage, setNewMessage] = useState("");
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);

  //Check if the length of the text has reached the line limit yet
  useEffect(() => {
    setIsLengthReached(messages.filter(message => message.type === "dialogue").length === lengthLimit)
  }, [messages])
  
  const handleSubmit = (event) => {
    event.preventDefault();

    if (newLine.trim()) {
      addMessage({ sender: "user", text: newLine, comment: newComment, type: "dialogue"});
      taskService
        .submitUserInput({inputData: { commentData: newComment}, text: newLine, ojective: theme})
        .then((returnedResponse) => {
          if (returnedResponse.text.match(/\[(.*?)\]/)) {
            addMessage({ 
              sender: "ai",
              text: returnedResponse.text,
              type: "dialogue"
            })
          } else {
            addMessage({ 
              sender: "ai",
              text: returnedResponse.text,
              type: "conversation"
            })
          }
        })
        .catch((error) => {
          console.log(error)
        });
      setNewLine("");
      setNewComment("");
    } else if (newComment.trim()) {
      addMessage({ sender: "user", text: "", comment: newComment, type: "conversation"});
      taskService
        .submitUserInput({inputData: { commentData: newComment}, text: "", ojective: theme})
        .then((returnedResponse) => {
          addMessage({ 
            sender: "ai",
            text: returnedResponse.text,
            type: "conversation"
          })
        })
        .catch((error) => {
          console.log(error)
        });
        setNewLine("");
        setNewComment("");
    } else {
      console.log("No data is being sent to the model");
    }
  };

  const handleThemeChange = (event) => setTheme(event.target.value)

  const chooseTheme = (event) => {
    if (!theme.trim()) {
      alert('Please enter a theme');
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    
    //Generate the first AI poem line after setting the theme, it works based on how the prompt is set up
    taskService
      .submitUserInput({
        inputData: { commentData: ""},
        text: "",
        objective: theme
      })
      .then((returnedResponse) => {
        addMessage({ 
          sender: "ai",
          text: returnedResponse.text,
          type: "dialogue"
        })
      })
      .catch((error) => {
        console.log(error)
      });
  };

  const toggleFinishButton = () => {
    toggleFinish();
    setIsFinishClicked(!isFinishClicked);
  }

  return (
    <div className="chat-space-wrapper">
      <h2>Discussion with AI</h2>
      <div className="chat-space">
        <div>
          <form onSubmit={chooseTheme} className="theme-input">
            <input 
                  type="text" 
                  disabled={isDisabled}
                  placeholder="Set a theme for the poem"
                  value={theme}
                  className={isDisabled ? "disabled" : ""}
                  onChange={handleThemeChange}
            />
            <button 
                type="button"
                disabled={isDisabled}
                className={isDisabled ? "disabled" : ""}
                onClick={chooseTheme}
                style={{
                  backgroundColor: "#4caf50"
                }}>
                Submit 
            </button>
          </form>
        </div>
        <div className="messages">
          {messages.map((msg, index) => (
            <ConversationItem key={index} message={msg} /> 
          ))}
        </div>
        {isLengthReached && 
        <span 
          style={{
            "color" : "#FF0000"
          }}>
          Thank you. Here is our final poem. Please click Finish to rate it!
        </span>
        }
        <div className="form-wrapper">
          <form onSubmit={handleSubmit}>
            <div className="input-form">  
              <textarea 
                value={newLine}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewLine(e.target.value)}
                placeholder="Add a line to the poem" 
              />
              <textarea 
                value={newComment}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewComment(e.target.value)} 
                placeholder="Send a message to the AI" 
              />
            </div>
          </form>
          <div className="button-group">
              <button type="submit" 
                style={{
                  backgroundColor: "#4caf50"
                }}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onClick={handleSubmit}> 
                Submit
              </button>
              <button type="submit" className="finish-button" 
                style={{
                  backgroundColor: isFinishClicked ? "#f44336" : "#6eb4ff",
                  "cursor": isFinishClicked ? "not-allowed" : "pointer"
                }}
                onClick={toggleFinishButton}> 
                {isFinishClicked ? "Cancel" : "Finish"}
              </button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
