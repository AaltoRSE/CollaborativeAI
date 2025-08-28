import { useState, useRef, useEffect } from 'react';
import Header from "./components/Header";
import Footer from "./components/Footer";
import FinishButton from './components/FinishButton';
import FeedbackForm from "./components/FeedbackForm";
import Dialogue from "./components/Dialogue";
import ConversationDisplay from "./components/ConversationDisplay"
import TaskDescription from './components/TaskDescription';
import FloorDescriptionForm from './components/FloorDescriptionForm';
import TutorialPopUp from './components/TutorialPopUp';
import SurveyButton from './components/SurveyButton'
import "./index.css";

const App = () => {
  const [isFinished, setIsFinished] = useState(false); 
  const [messages, setMessages] = useState([])
  const [isFinishClicked, setIsFinishClicked] = useState(false);
  const [isRatingSubmitted, setIsRatingSubmitted] = useState(false);
  const [isDisabled, setIsDisabled] = useState(false);
  const [floorDescription, setFloorDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const viewPointRef = useRef(null);
  
  useEffect(() => {
    if (isFinished) {
      if (viewPointRef.current) {
        viewPointRef.current.scrollIntoView({ behavior: "smooth", block: "center"});
      }
    }
  }, [isFinished]);

  const addMessage = (message) => {
    setMessages(prevMessages => prevMessages.concat(message));
  };

  const toggleFinish = () => {
    setIsFinished(!isFinished);
    setIsFinishClicked(!isFinishClicked);
  }
  
  return (
    <>
      <Header />
      <TaskDescription />
      <SurveyButton />
      {/* <TutorialPopUp /> */}
      <FloorDescriptionForm floorDescription={floorDescription} setFloorDescription={setFloorDescription} messages={messages} isDisabled={isDisabled} setIsDisabled={setIsDisabled} setIsLoading={setIsLoading} addMessage={addMessage}/>
      <div className="main-interaction">
        {(isRatingSubmitted || isFinishClicked) && (
          <div className="main-interaction-overlay"> </div>
        )}
        <Dialogue isLoading={isLoading} setIsLoading={setIsLoading} setFloorDescription={setFloorDescription} messages={messages} addMessage={addMessage} setIsDisabled={setIsDisabled}/>
        <ConversationDisplay isLoading={isLoading} setIsLoading={setIsLoading} setFloorDescription={setFloorDescription} isDisabled={isDisabled} messages={messages} addMessage={addMessage} />
      </div>
      <FinishButton messages={messages} isFinishClicked={isFinishClicked} isRatingSubmitted={isRatingSubmitted} toggleFinish={toggleFinish} />
      {isFinished && <FeedbackForm viewPointRef={viewPointRef} isRatingSubmitted={isRatingSubmitted} setIsRatingSubmitted={setIsRatingSubmitted}/>}
      <Footer />
    </>
  );
};

export default App;
