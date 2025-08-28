import { useEffect, useRef } from 'react';
import DialogueItem from "./DialogueItem";
import Editor from '@monaco-editor/react';

const Dialogue = ({ isLoading, messages }) => {
  const messagesRef = useRef(null);

  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])

  return (
    <div className="dialogue-wrapper">
      <h2>Board</h2>
      <div className="dialogue">
        <div className="dialogue-content" ref={messagesRef}>
          {/* <Editor
            height="300px"
            language={"javascript"}
            value={"console.log('Hello')"}
            options={{
              readOnly: true,
              minimap: { enabled: false },
              lineNumbers: "on",
              fontSize: 14,
              scrollBeyondLastLine: false,
              contextmenu: false,
            }}
          /> */}
          {messages
            .map((msg, idx) => ({ ...msg, originalIndex: idx })) // Preserve original index
            .filter(msg => msg.text !== "" && msg.text !== null)
            .map((msg) => (
              <DialogueItem
                key={msg.originalIndex} // Use original index as key if needed
                idx={msg.originalIndex} // Pass original index as `idx`
                message={msg}
              />
            ))}
        </div>
        {isLoading && <div>Waiting for response...</div>} 
      </div>
    </div>
  );
};

export default Dialogue;
