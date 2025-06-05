import { useEffect, useRef } from 'react';
import FloorplanGame from './FloorplanGame';

const Dialogue = ({ setIsLoading, messages, addMessage, isLoading, isDisabled, setIsDisabled }) => {
  const messagesRef = useRef(null);
  useEffect(() => {
    if (messagesRef.current) {
      messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    }    
  }, [messages])



  return (
    <div className="dialogue-wrapper">
      <h2>Floor plan</h2>
      <div className="dialogue">
        {(isLoading) && (
          <div className="floorplan-interaction-overlay"> 
            <h2>Loading...</h2>
          </div>
        )}
        <FloorplanGame messages={messages} addMessage={addMessage} setIsLoading={setIsLoading} isDisabled={isDisabled} setIsDisabled={setIsDisabled} />
      </div>
    </div>
  );
};

export default Dialogue;
