import taskService from '../services/task'

const ThemeForm = ({ theme, setTheme, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  const parsePoetryAndComment = (input) => {
    let poetryLine = "";
    let comment = "";
    input = input.trim();

    if (input.includes('[')) {
      let startBracketIndex = input.indexOf('[');
      let endBracketIndex = input.indexOf(']');
      
      if (startBracketIndex !== -1 && endBracketIndex !== -1) {
        poetryLine = input.substring(startBracketIndex + 1, endBracketIndex).trim();
        let commentBeforeBracket = input.substring(0, startBracketIndex).trim();
        let commentAfterBracket = input.substring(endBracketIndex + 1).trim();

        if (commentBeforeBracket && commentAfterBracket) {
          comment = `${commentBeforeBracket} ${commentAfterBracket}`.trim();
        } else {
          comment = commentBeforeBracket || commentAfterBracket;
        }
      } else {
        comment = input
      }
    } else {
      comment = input
    }
    
    return { poetryLine, comment };
  }

  const checkAndAddMessage = (sender, text, comment, type) => {
    text = (typeof text === 'string' && text.trim()) ? text : null;
    comment = (typeof comment === 'string' && comment.trim()) ? comment : null;

    if (text === null && comment === null) {
      console.log("no message");
    } else {
      addMessage({ sender: sender, text: text, comment: comment, type: "dialogue"}); 
    }
  }

  const chooseTheme = (event) => {
    if (!theme.trim()) {
      alert("Please enter a theme");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    //Generate the first AI poem line after setting the theme, it works based on how the prompt is set up
    taskService
      .submitUserInput({
        inputData: { 
          comment: true,
          poem: []
        },
        text: "Write the first line of the poem",
        objective: theme
      })
      .then((returnedResponse) => {
        let parsed = parsePoetryAndComment(returnedResponse.text)
        checkAndAddMessage("ai", parsed.poetryLine, parsed.comment, "dialogue")
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
      <div className='theme-wrapper'>
        <form onSubmit={chooseTheme} className="theme-input">
          <label> <h3>Set theme</h3></label>
          <input 
            type="text" 
            disabled={isDisabled}
            placeholder="Set a theme for the poem"
            value={theme}
            onChange={(event) => setTheme(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="theme-submit-btn"
            onClick={chooseTheme}>
            Submit 
          </button>
        </form>
      </div>
    </>
  );
};

export default ThemeForm;
