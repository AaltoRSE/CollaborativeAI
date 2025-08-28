import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const ConversationalItem = ({ message }) => {
  const messageClass = message.sender === "user" ? "user-message" : "ai-message";
  const avatarClass = message.sender === "user" ? "avatar-user" : "avatar-ai";
  const avatarText = message.sender === "user" ? "You" : "AI";

  return (
    <>
      <div className={`dialogue-poem ${messageClass}`}>
        {message.sender === "user" ? (
          <>
            <ReactMarkdown
              children={message.message}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            />
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
          </>
        ) : (
          <>
            <div className={`avatar ${avatarClass}`}> {avatarText} </div>
            <ReactMarkdown
              children={message.message}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            />
          </>
        )}
      </div>
    </>
    
  );
};

export default ConversationalItem;
