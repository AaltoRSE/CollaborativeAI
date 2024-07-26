import { useState, useEffect } from 'react';
import ConversationDisplay from "./components/ConversationDisplay";
import Dialogue from "./components/Dialogue";
import TaskDescription from "./components/TaskDescription";
import Header from "./components/Header";
import Footer from "./components/Footer";
import FeedbackForm from "./components/FeedbackForm";
import "./index.css";

const App = () => {
  // const [messages, setMessages] = useState([
  //   { sender: "ai", text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", comment: "", type: "dialogue"},
  //   { sender: "user", text: "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", comment: "", type: "dialogue"},
  //   { sender: "ai", text: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.", comment: "", type: "dialogue"},
  //   { sender: "user", text: "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet. It uses a dictionary of over 200 Latin words, combined with a handful of model sentence structures, to generate Lorem Ipsum which looks reasonable. The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.", comment: "", type: "dialogue"}
  // ]);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    console.log(messages)
  }, [messages])

  const [isFinished, setIsFinished] = useState(false);

  const addMessage = (message) => {
    setMessages(prevMessages => prevMessages.concat(message));
  };

  const toggleFinish = () => {
    setIsFinished(!isFinished);
  };

  return (
    <>
      <Header />
      <TaskDescription />
      <div className="main-interaction">
        <Dialogue messages={messages} setMessages={setMessages} />
        <ConversationDisplay toggleFinish={toggleFinish} messages={messages} addMessage={addMessage} />
      </div>
      {isFinished ? <FeedbackForm /> : <div className="feedback-placeholder"> </div>}
      <Footer />
    </>
  );
};

export default App;
