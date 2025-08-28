import { useState, useEffect, useRef } from 'react';
import ConversationItem from "./ConversationItem";
import taskService from '../services/task'
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import Editor from '@monaco-editor/react';

const ConversationDisplay = ({ isLoading, setIsLoading, topicDescription, isDisabled, messages, addMessage }) => {
  const [newComment, setNewComment] = useState("");
  const messagesRef = useRef(null);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])

  const textareaRef = useRef(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!newComment.trim()) {
      return;
    }
    setIsLoading(true);
    addMessage({ sender: "user", message: newComment}); 
    // checkAndAddMessage("user", null, newComment,"dialogue");   

    taskService
      .submitUserInput({
        inputData: {
          comment: true,
          messages: messages
        }, 
        text: newComment, 
        ojective: topicDescription
      })
      .then((returnedResponse) => {
        let parsed = JSON.parse(returnedResponse.text)
        addMessage({ sender: "ai", message: parsed.message})
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
      <h2>Board</h2>
      <div className="chat-space">
        <div className="messages" ref={messagesRef}>
          {/* {messages
            .filter(msg => msg.comment !== "" && msg.comment !== null)
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          } */}
          {messages
            .map((msg, index) => (
              <ConversationItem key={index} message={msg} /> 
            ))
          }
        </div>
        {isLoading && <div>Waiting for response...</div>} 
          <div className="form-wrapper">
            <form onSubmit={handleSubmit} className="input-form">
              <textarea 
                value={newComment}
                ref={textareaRef}
                disabled={!isDisabled || isLoading}
                onChange={(event) => setNewComment(event.target.value)} 
                placeholder="Send a message to the AI. Wrap your code inside ``` ```" 
              />
              <button type="submit" 
                disabled={!isDisabled || isLoading}
                onClick={handleSubmit}> 
                Send
              </button>
            </form>
          </div>
          {/* <div className='preview-box-conversation'>
            <strong>Preview:</strong>
            <div style={{ marginTop: '5px' }}>
              <ReactMarkdown
                children={newComment}
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeKatex]}
              />
            </div>
          </div> */}
      </div>
    </div>
  );
};

export default ConversationDisplay;
