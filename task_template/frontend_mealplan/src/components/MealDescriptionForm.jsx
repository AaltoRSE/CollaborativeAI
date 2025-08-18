import taskService from '../services/task'

const MealDescriptionForm = ({ mealDescription, setMealDescription, messages, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  const chooseMealDescription = (event) => {
    if (!mealDescription.trim()) {
      alert("Please enter the description of your preferred meal plan");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    taskService
      .submitUserInput({
        inputData: {
          comment: true,
          plans: []
        },
        text: "Give me a meal plan based on the description",
        objective: mealDescription
      })
      .then((returnedResponse) => {
        let parsed = JSON.parse(returnedResponse.text)
        addMessage({ sender: "ai", mealplan: parsed.mealplan, comment: parsed.comment})
        setIsLoading(false)
      })
      .catch((error) => {
        console.log(error)
      });
  };

  return (
    <>
      <div className='meal-description-wrapper'>
        <form onSubmit={chooseMealDescription} className="meal-description-input">
          <h3 style={{"maxWidth": "200px"}}>Tell me your meal plan description </h3>
          <textarea 
            type="text"
            style={{"minWidth": "180px", "minHeight": "80px"}}
            disabled={isDisabled}
            placeholder="What kind of meal plan would you like to have?"
            value={mealDescription}
            onChange={(event) => setMealDescription(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="meal-description-submit-btn"
            onClick={chooseMealDescription}>
            Submit 
          </button>
        </form>
      </div>
    </>
  );
};

export default MealDescriptionForm;
