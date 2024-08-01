import { useState, useEffect } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task';
import { lengthLimit } from '../utils/config';

const ConversationDisplay = ({ toggleFinish, messages, addMessage, formData }) => {
  const [newLine, setNewLine] = useState("");
  const [newComment, setNewComment] = useState("");
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [theme, setTheme] = useState("");
  const [isLengthReached, setIsLengthReached] = useState(false);

  function checkAndAddMessage(sender, text, comment, type){
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;
  
    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue" });
    }
  }

  useEffect(() => {
    setIsLengthReached(messages.filter(msg => msg.text !== "" && msg.text !== null).length === lengthLimit);
  }, [messages]);

  function parsePoetryAndComment(input) {
    let poetryLine = "";
    let comment = "";

    input = input.trim();

    if (input.startsWith('[')) {
      let endBracketIndex = input.indexOf(']');
      if (endBracketIndex !== -1) {
        poetryLine = input.substring(1, endBracketIndex).trim();
        if (endBracketIndex + 1 < input.length) {
          comment = input.substring(endBracketIndex + 1).trim();
        }
      }
    } else {
      comment = input;
    }

    console.log("Parsed: ", poetryLine, ", ", comment);

    return { poetryLine, comment };
  }

  const handleSubmit = (event) => {
    event.preventDefault();

    checkAndAddMessage("user", newLine, newComment, "dialogue");

    taskService
      .submitUserInput({ inputData: { commentData: newComment, reqType: "chat"}, text: newLine, objective: theme })
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

  const handleThemeChange = (event) => setTheme(event.target.value)

  const chooseTheme = (event) => {
    if (!theme.trim()) {
      alert('Please enter a theme');
      return;
    }
    event.preventDefault();
    setIsDisabled(true);

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
  };

  return (
    <div className="chat-space-wrapper">
      <h2>Chat with the AI</h2>
      <div className="chat-space">
        <div className="messages">
          {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} />
            ))
          }
        </div>
        <div className="form-wrapper">
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'stretch', width: "100%" }}>
            <div className="input-form" style={{ display: 'flex', alignItems: 'stretch' }}>
              <textarea
                value={newComment}
                onChange={(event) => setNewComment(event.target.value)}
                placeholder="Send a message to the AI"
                style={{ height: "100px", resize: "none", flexGrow: 1, width: "80%" }}
              />
              <button type="submit"
                style={{
                  backgroundColor: "#4caf50",
                  height: "100px",
                  width: "15%",
                  maxWidth: "150px",
                  borderTop: "10px"
                }}>
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ConversationDisplay;
