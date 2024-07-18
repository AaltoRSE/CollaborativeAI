import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("")
  const [isLengthReached, setIsLengthReached] = useState(false)

  //Check if the length of the poem has reached 9 lines yet
  useEffect(() => {
    setIsLengthReached(messages.length === 9) //It can be different number depends on what we want to achieve here
  }, [messages])

  const handleSubmit = (event) => {
    const newMessageObject = {
      inputData: { commentData: newComment},
      text: newLine,
      ojective: theme
    }
    event.preventDefault();
    if (newLine.trim()) {
      addMessage({ sender: "user", text: newLine });
      taskService
        .submitUserInput(newMessageObject)
        .then((returnedResponse) => {
          addMessage({ 
            sender: "ai",
            text: returnedResponse.text
          })
        })
        .catch((error) => {
          console.log(error)
        });
      setNewLine("");
      setNewComment("");
    }
  };

  const handleThemeChange = (event) => setTheme(event.target.value)

  const chooseTheme = () => {
    if (!theme.trim()) {
      alert('Please enter a theme');
      return;
    }
    
    console.log('Theme set:', theme);
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
          text: returnedResponse.text
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
              onClick={chooseTheme} 
              disabled={isDisabled}
              className={isDisabled ? "disabled" : ""}
              style={{
                "background-color": "#4caf50"
              }}>
              Submit 
          </button>
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
          <form onClick={handleSubmit}>
            <div className="input-form">
              <input 
                type="text" 
                value={newComment}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewComment(e.target.value)} 
                placeholder="Send a message to the AI" 
              />
              <input 
                type="text" 
                value={newLine} 
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(e) => setNewLine(e.target.value)} 
                placeholder="Add a line to the poem" 
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
