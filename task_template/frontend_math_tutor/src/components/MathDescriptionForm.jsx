import taskService from '../services/task'
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';

const TopicDescriptionForm = ({ topicDescription, setTopicDescription, messages, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  const chooseTopicDescription = (event) => {
    if (!topicDescription.trim()) {
      alert("Please enter the description of your math topic");
      return;
    }
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
        console.log(returnedResponse.text)
        let parsed = JSON.parse(returnedResponse.text)
        addMessage({ sender: "ai", message: parsed.message})
        setIsLoading(false)
      })
      .catch((error) => {
        if (error.response && error.response.status === 429) {
          alert(error.response.data.error);
        } else {
          console.log(error);
        }
        setIsLoading(false)
        setIsDisabled(false)
      });
  };

  return (
    <>
      <div className='topic-description-wrapper'>
        <form onSubmit={chooseTopicDescription} className="topic-description-input">
          <h3 style={{"maxWidth": "200px", "marginRight": "15px"}}>Which concept do you want to learn? </h3>
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
