import taskService from '../services/task'
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const TopicDescriptionForm = ({ topicDescription, setTopicDescription, messages, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  function parsePoetryAndComment(input) {
    // Initialize variables to store the parsed parts
    let message = "";
    let comment = "";
  
    // Trim the input to remove leading/trailing whitespace
    input = input.trim();
  
    // Check if the input starts with a '[' character
    if (input.startsWith('[')) {
        // Find the closing ']' character
        let endBracketIndex = input.indexOf(']');
        
        // If a closing ']' is found, extract the poetry line
        if (endBracketIndex !== -1) {
            message = input.substring(1, endBracketIndex).trim();
            // Extract the comment part if there is any text after the closing ']'
            if (endBracketIndex + 1 < input.length) {
                comment = input.substring(endBracketIndex + 1).trim();
            }
        }
    } else {
        // If the input doesn't start with '[', consider the whole input as a comment
        comment = input;
    }
  
    // console.log("Parsed: ", message, ", ", comment)
  
    return { message, comment };
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

  const chooseTopicDescription = (event) => {
    if (!topicDescription.trim()) {
      alert("Please enter the description of your math topic");
      return;
    }
    console.log(topicDescription)
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    taskService
      .submitUserInput({
        inputData: {
          comment: true,
          messages: []
        },
        text: "Start explaining this math topic/problem",
        objective: topicDescription
      })
      .then((returnedResponse) => {
        let parsed = parsePoetryAndComment(returnedResponse.text)
        checkAndAddMessage("ai", parsed.message, parsed.comment, "dialogue")
        setIsLoading(false)
      })
      .catch((error) => {
        console.log(error)
      });
  };

  return (
    <>
      <div className='topic-description-wrapper'>
        <form onSubmit={chooseTopicDescription} className="topic-description-input">
          <h3 style={{"maxWidth": "200px"}}>Which concept do you want to learn? </h3>
          <textarea 
            type="text"
            style={{"minWidth": "180px", "minHeight": "80px"}}
            disabled={isDisabled}
            placeholder="What do you want to learn? Type math equation in Markdown: $\sqrt{a^2 + b^2}$"
            value={topicDescription}
            onChange={(event) => setTopicDescription(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="topic-description-submit-btn"
            onClick={chooseTopicDescription}>
            Submit 
          </button>
        </form>
        <div className='preview-box'>
          <strong>Preview:</strong>
          <div style={{ marginTop: '5px'}}>
            <ReactMarkdown
              children={topicDescription}
              remarkPlugins={[remarkMath]}
              rehypePlugins={[rehypeKatex]}
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default TopicDescriptionForm;
