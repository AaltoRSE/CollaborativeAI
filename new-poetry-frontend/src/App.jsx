import { useState } from "react";
import ConversationDisplay from "../components/ConversationDisplay";
import Dialogue from "../components/Dialogue";
import TaskDescription from "../components/TaskDescription";
import Header from "../components/Header";
import Footer from "../components/Footer";
import FeedbackForm from "../components/FeedbackForm";

import "./index.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isFinished, setIsFinished] = useState(false);

  const addMessage = (msg) => {
    setMessages(prevMessages => prevMessages.concat(msg));
  };

  const toggleFinish = () => {
    setIsFinished(!isFinished);
  };

  return (
    <>
      <Header />
      <TaskDescription />
      <div className="main-interaction">
        <Dialogue messages={messages} />
        <ConversationDisplay toggleFinish={toggleFinish} messages={messages} addMessage={addMessage} />
      </div>
      {isFinished ? <FeedbackForm /> : <div className="feedback-placeholder"> </div>}
      <Footer />
    </>
  );
};

export default App;
