import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'
import { lengthLimit } from '../../config';

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  const [newMessage, setNewMessage] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);

  //Check if the length of the text has reached the line limit yet
  useEffect(() => {
    setIsLengthReached(messages.length === lengthLimit)
    console.log(messages)
  }, [messages])

  const handleSubmit = (event) => {
    event.preventDefault();

    let newLine = ""
    const poemLine = newMessage.match(/\[(.*?)\]/);
    if (newMessage.trim() && poemLine) {
      newLine = poemLine[1];
      addMessage({ sender: "user", text: newLine, comment: newMessage, type: "dialogue"});
      taskService
        .submitUserInput({inputData: { commentData: newMessage}, text: newLine, ojective: theme})
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
      setNewMessage("");
    } else if (!poemLine) {
      addMessage({ sender: "user", text: "", comment: newMessage, type: "conversation"});
      taskService
        .submitUserInput({inputData: { commentData: newMessage}, text: "", ojective: theme})
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
      setNewMessage("");
    } else {
      console.log("Error")
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
    
    //Generate the first AI poem line after setting the theme
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
        <div className="theme-input">
          <form onSubmit={chooseTheme}>
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
                style={{
                  "background-color": "#4caf50"
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
              {/* <input 
                type="text" 
                value={newComment}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewComment(e.target.value)} 
                placeholder="Send a message to the AI" 
              /> */}
              <input 
                type="text" 
                value={newMessage} 
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewMessage(e.target.value)} 
                placeholder="Send a message to the AI" 
              />
            </div>
          </form>
          <div className="button-group">
              <button type="submit" 
                style={{
                  "background-color": "#4caf50"
                }}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onClick={handleSubmit}> 
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
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
