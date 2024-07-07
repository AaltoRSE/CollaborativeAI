import { useState } from 'react';
import ConversationDisplay from '../components/ConversationDisplay';
import Dialogue from '../components/Dialogue';
import TaskDescription from '../components/TaskDescription';
import Header from '../components/Header';
import Footer from '../components/Footer';

import './index.css';

const App = () => {
  const [messages, setMessages] = useState([]);

  const addMessage = (msg) => {
    setMessages(prevMessages => prevMessages.concat(msg));
  };

  return (
    <>
      <Header />
      <TaskDescription />
      <div className="main-interaction">
        <Dialogue messages={messages} />
        <ConversationDisplay messages={messages} addMessage={addMessage} />
      </div>
      <Footer />
    </>
  );
};

export default App;
