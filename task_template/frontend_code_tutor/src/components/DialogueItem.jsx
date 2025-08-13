import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const DialogueItem = ({ message, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  return (
    <>
      <div className={`dialogue-poem ${messageClass}`}>
        <ReactMarkdown
          children={message.text}
          remarkPlugins={[remarkMath]}
          rehypePlugins={[rehypeKatex]}
        />
      </div>
    </>
  );
};

export default DialogueItem;
