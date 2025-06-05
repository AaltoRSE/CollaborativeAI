import taskService from '../services/task'

const FloorDescriptionForm = ({ floorDescription, setFloorDescription, messages, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let floor = "";
    let comment = "";
  
    // Trim the input to remove leading/trailing whitespace
    input = input.trim();
  
    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            floor = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }
  
    // console.log("Parsed: ", floor, ", ", comment)
  
    return { floor, comment };
  }
  
  function checkAndAddMessage(sender, text, comment, type) {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;
  
    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const chooseFloorDescription = (event) => {
    if (!floorDescription.trim()) {
      alert("Please enter the description for your floor");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    taskService
      .submitUserInput({
        inputData: {
          comment: true,
          floorplans: []
        },
        text: "Suggest the first move based on the given floor plan description",
        objective: floorDescription
      })
      .then((returnedResponse) => {
        console.log(returnedResponse)
        let parsed = parsePoetryAndComment(returnedResponse.text)
        checkAndAddMessage("ai", parsed.floor, parsed.comment, "dialogue")
        setIsLoading(false)
      })
      .catch((error) => {
        console.log(error)
      });
  };

  return (
    <>
      <div className='floor-description-wrapper'>
        <h1 style={{textAlign:'center'}}>Let’s design the bedroom together</h1>
        {/* <form onSubmit={chooseFloorDescription} className="floor-description-input">
          <h3 style={{"maxWidth": "200px"}}>Which room are you designing? </h3>
          <textarea 
            type="text"
            disabled={isDisabled}
            placeholder="What is the room you are designing"
            value={floorDescription}
            onChange={(event) => setFloorDescription(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="floor-description-submit-btn"
            onClick={chooseFloorDescription}>
            Submit 
          </button>
        </form> */}
      </div>
    </>
  );
};

export default FloorDescriptionForm;
