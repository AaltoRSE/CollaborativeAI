import { useState } from 'react';
import ConversationDisplay from "./components/ConversationDisplay";
import Dialogue from "./components/Dialogue";
import TaskDescription from "./components/TaskDescription";
import Header from "./components/Header";
import Footer from "./components/Footer";
import FeedbackForm from "./components/FeedbackForm";
import SetupDialog from './components/SetupDialog';
import taskService from './services/task';
import "./index.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isFinished, setIsFinished] = useState(false);
  const [showSetupDialog, setShowSetupDialog] = useState(true);
  const [formData, setFormData] = useState({
    name: '',
    style: '',
    tone: '',
    reference: ''
});

  const addMessage = (message) => {
    setMessages(prevMessages => prevMessages.concat(message));
  };

  const toggleFinish = () => {
    setIsFinished(!isFinished);
  };

  const closeSetupDialog = () => {
    setShowSetupDialog(!showSetupDialog);
    taskService
      .submitUserInput({ inputData: { reqType: "Hello", name: formData.name, style: formData.style, tone: formData.tone, reference : formData.reference }, text : "", objective : "" })
      .then((returnedResponse) => {
        addMessage({ sender: "ai", text: "", comment: returnedResponse.text, type: "dialogue" });
        console.log(returnedResponse.text);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
        ...prevData,
        [name]: value
    }));
};


  return (
    <>
      <Header />
      <SetupDialog show = {showSetupDialog} onClose = {closeSetupDialog} formData = {formData} handleChange={handleChange} />
      <div className="main-interaction">
        <Dialogue messages={messages} setMessages={setMessages} formData={formData} addMessage={addMessage} />
        <ConversationDisplay toggleFinish={toggleFinish} messages={messages} addMessage={addMessage} formData = {formData} />
      </div>
      {isFinished ? <FeedbackForm /> : <div className="feedback-placeholder"> </div>}
      <Footer />
    </>
  );
};

export default App;
