import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task';
import { lengthLimit } from '../utils/config';

const ConversationDisplay = ({ toggleFinish, messages, addMessage }) => {
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);
  const poemLines = messages
  .filter(msg => msg.text !== "" && msg.text !== null)
  .map(msg => msg.text);
  const discussionLines = messages
  .filter(msg => msg.comment !== "" && msg.comment !== null)
  .map(msg => msg.comment);

  // Check if the length of the text has reached the line limit yet
  useEffect(() => {
    setIsLengthReached(messages.filter(msg => msg.text !== "" && msg.text !== null).length === lengthLimit);
  }, [messages]);

  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let poetryLine = "";
    let comment = "";

    // Trim the input to remove leading/trailing whitespace
    input = input.trim();

    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
      // Find the closing ']' character
      let endBracketIndex = input.indexOf(']');
      
      // If a closing ']' is found, extract the poetry line
      if (endBracketIndex !== -1) {
          poetryLine = input.substring(1, endBracketIndex).trim();
          // Extract the comment part if there is any text after the closing ']'
          if (endBracketIndex + 1 < input.length) {
              comment = input.substring(endBracketIndex + 1).trim();
          }
      }
  } else {
      // If the input doesn't start with '[', consider the whole input as a comment
      comment = input;
  }

    console.log("Parsed: ", poetryLine, ", ", comment);

    return { poetryLine, comment };
  }

  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue" });
    }
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    checkAndAddMessage("user", newLine, newComment, "dialogue");

    if (isLengthReached) {
      newComment += " The poem is finished. Do NOT add a new poetry line.";
    }

    taskService
      .submitUserInput({ inputData: { commentData: newComment }, text: newLine, objective: theme })
      .then((returnedResponse) => {
        let parsed = parsePoetryAndComment(returnedResponse.text);
        checkAndAddMessage("ai", parsed.poetryLine, parsed.comment, "dialogue");
      })
      .catch((error) => {
        console.log(error);
      });

    setNewLine("");
    setNewComment("");
  };

  const chooseTheme = (event) => {
    if (!theme.trim()) {
      alert("Please enter a theme");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);

    // Generate the first AI poem line after setting the theme, it works based on how the prompt is set up
    taskService
      .submitUserInput({
        inputData: { commentData: "" },
        text: "",
        objective: theme
      })
      .then((returnedResponse) => {
        let parsed = parsePoetryAndComment(returnedResponse.text);
        checkAndAddMessage("ai", parsed.poetryLine, parsed.comment, "dialogue");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const toggleFinishButton = () => {
    toggleFinish();
    setIsFinishClicked(!isFinishClicked);
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); 
      handleSubmit(event); 
    }
  };  

  const exportPoem = () => {
    const blob = new Blob([poemLines.join('\n')], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'poem.txt';
    a.click();
    URL.revokeObjectURL(url);
  }

  const exportDiscussion = () => {
    const blob = new Blob([discussionLines.join('\n')], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'discussion.txt';
    a.click();
    URL.revokeObjectURL(url);
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
                  onChange={(event) => setTheme(event.target.value)}
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
          {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          }
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
                onChange={(event) => setNewLine(event.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Add a line to the poem" 
              />
              <textarea 
                value={newComment}
                disabled={isLengthReached}
                className={isLengthReached ? "disabled" : ""}
                onChange={(event) => setNewComment(event.target.value)} 
                onKeyDown={handleKeyPress}
                placeholder="Send a message to the AI" 
              />
            </div>
          </form>
          <div className="button-group">
              <button type="button" className="finish-button" 
                style={{
                  backgroundColor: isFinishClicked ? "#f44336" : "#6eb4ff",
                  cursor: isFinishClicked ? "not-allowed" : "pointer"
                }}
                onClick={toggleFinishButton}> 
                {isFinishClicked ? "Cancel" : "Finish"}
              </button>
              <button type="button" 
                style={{
                  backgroundColor: "#ff9800"
                }}
                onClick={exportPoem}> 
                Export Poem
              </button>
              <button type="button" 
                style={{
                  backgroundColor: "#ff9800"
                }}
                onClick={exportDiscussion}> 
                Export Discussion
              </button>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
