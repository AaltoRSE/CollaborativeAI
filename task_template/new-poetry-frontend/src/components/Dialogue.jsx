import { useEffect, useRef, useState } from 'react';
import Quill from 'quill';
import taskService from '../services/task';
import Popup from './Popup';

const Dialogue = ({ messages, setMessages, formData, addMessage }) => {
  const quillRef = useRef(null);
  const tooltipRef = useRef(null);
  const oldTextRef = useRef('');
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [selectedOption, setSelectedOption] = useState('movie');
  const [popupContent, setPopupContent] = useState('Hello World');
  const [showPopup, setShowPopup] = useState(false);
  
  // Add event listener for mouse move to track mouse position
  const handleMouseMove = (event) => {
    setMousePosition({ x: event.clientX, y: event.clientY });
    console.log("Test Mouse Move: " + mousePosition.x + " ")
  };
  
  useEffect(() => {
    // Initialize Quill editor
    const quill = new Quill('#editor', {
      theme: 'snow'
    });
    quillRef.current = quill;
    
    // Add event listener for text selection
    quill.on('selection-change', (range) => {
      if (range && range.length > 0) {
        showTooltip();
      } else {
        hideTooltip();
      }
    });
    document.getElementById('editor').addEventListener('mousemove', handleMouseMove);
    const intervalId = setInterval(timerCheck, 10000);
  }, []);

  const showTooltip = () => {
    const quill = quillRef.current;
    const range = quill.getSelection();
    
    if (range) {
      // Get the bounds of the selected text
      const bounds = quill.getBounds(range.index, range.length);
      
      // Calculate the tooltip position
      const tooltip = tooltipRef.current;
      tooltip.style.display = 'block';
      tooltip.style.left = `${bounds.left}px`;
      tooltip.style.top = `${bounds.top + 20}px`; // Position above the selection
    }
  };

  const hideTooltip = () => {
    const tooltip = tooltipRef.current;
    tooltip.style.display = 'none';
  };

  const handleReplace = () => {
    const quill = quillRef.current;
    const range = quill.getSelection();
    if (range) {
      var selectedText = quill.getText(range.index, range.length);
      var select_begin = range.index
      var select_length = range.length
      const current_text = getTextContent();
      const textAfterSelect = quill.getText(range.index+range.length, current_text.length)

      taskService
        .submitUserInput({inputData: {reqType: "replace", amount : selectedText, name : formData.name, style : formData.style, tone: formData.tone, reference : formData.reference}, text : getTextContent()})
        .then((returnedResponse) => {
          quill.deleteText(select_begin, select_length);
          quill.insertText(select_begin, returnedResponse.text);
          quill.formatText(select_begin, returnedResponse.text.length, {'color' : 'green'});
          quill.format('color', 'black');
        })
        .catch((error) => {
          console.log(error);
        });
    }
    hideTooltip();
  };

  const getTextContent = () => {
    const quill = quillRef.current;
    if (quill) {
      const text = quill.getText();
      console.log("got: " + text);
      return text;
    }
    return '';
  };

  // getSemanticHTML

  
  const requestText = (amount) =>{
    const current_text = getTextContent();
    taskService
      .submitUserInput({ inputData: { reqType : "complete", amount: amount, name : formData.name, style : formData.style, tone: formData.tone, reference : formData.reference}, text : getTextContent()})
      .then((returnedResponse) => {
        const quill = quillRef.current;
        quill.insertText(current_text.length - 1, returnedResponse.text);
        quill.formatText(current_text.length - 1, current_text.length - 1 + returnedResponse.text.length, {'color' : 'blue'})
        quill.format('color', 'black');
      })
      .catch((error) => {
        console.log(error);
      });
  }

  const requestAnalysis = () =>{
    const quill = quillRef.current;
    const current_text = getTextContent();
    taskService
      .submitUserInput({ inputData: { reqType : "analyse", name : formData.name, style : formData.style, tone: formData.tone, reference : formData.reference}, text : getTextContent()})
      .then((returnedResponse) => {
        console.log(returnedResponse.text)
        const quill = quillRef.current;
        var array = returnedResponse.text.split(/\r?\n/)
        for (let index = 0; index < array.length; index++) {
          //if (array[index][0] == "-") {
          //  addMsg(array[index])
          //}
          //else {
            highlightText(array[index])          
          //}
        }
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function timerCheck() {
    let newText = getTextContent();
    if(newText === oldTextRef.current){
      console.log('Function executed at', new Date().toLocaleTimeString());
    }
    else{
      console.log("This would have called GPT");
      requestAnalysis();
    }
    oldTextRef.current = newText;
  }

  const highlightText = (searchString) => {
    const quill = quillRef.current;
    const text = quill.getText();
    const length = searchString.length;
    let index = 0;

    quill.formatText(0, text.length, { 'background': '' });

    while ((index = text.indexOf(searchString, index)) !== -1) {
      quill.formatText(index, length, { 'background': 'orange' });
      index += length;
    }
  };

  const addMsg = (text) => {
  }


const handleDropdownChange = (event) => {
  setSelectedOption(event.target.value);
};

const handleDropdownButtonClick = () => {
  // Logic for handling the button click next to the dropdown
  console.log('Selected option:', selectedOption);
  // Call a function with the selected option
  requestTransform(selectedOption);
};

const requestTransform = (option) =>{
  const quill = quillRef.current;
  const current_text = getTextContent();
  taskService
    .submitUserInput({ inputData: { reqType : "movie", name : formData.name, style : formData.style, tone: formData.tone, reference : formData.reference}, text : getTextContent()})
    .then((returnedResponse) => {
      setPopupContent(returnedResponse.text); // assuming returnedResponse.markdown contains the markdown content
      setShowPopup(true);
    })
    .catch((error) => {
      console.log(error);
    });
}

  return (
    <div>
      <div className="dialogue-wrapper">
        <h2>Our Story</h2>
        <div className="dialogue">
          <div id="editor">

          </div>
          <div ref={tooltipRef} className="tooltip">
            <button onClick={handleReplace}>Replace</button>
          </div>
        </div>
        <div className="button-wrapper">
            <button type="button" className="request_button" onClick={() => requestText("with a sentence")}>Request sentence</button>
            <button type="button" className="request_button" onClick={() => requestText("with a paragraph")}>Request paragraph</button>
            <button type="button" className="request_button" onClick={() => requestText("until the end")}>Request the rest of the story</button>
        </div>
      </div>
      <div className="dropdown-wrapper">
          <select className="dropdown" value={selectedOption} onChange={handleDropdownChange}>
            <option value="movie">Movie</option>
            <option value="social promo">Social promo</option>
          </select>
          <button className="dropdown-button" onClick={() => handleDropdownButtonClick()}>Export</button>
        </div>
      {showPopup && <Popup content={popupContent} onClose={() => setShowPopup(false)} />}
    </div>
  );
};

export default Dialogue;
