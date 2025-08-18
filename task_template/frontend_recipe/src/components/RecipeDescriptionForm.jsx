import taskService from '../services/task'

const RecipeDescriptionForm = ({ recipeDescription, setRecipeDescription, messages, isDisabled, setIsDisabled, setIsLoading, addMessage }) => {
  const chooseRecipeDescription = (event) => {
    if (!recipeDescription.trim()) {
      alert("Please enter the name of the recipe");
      return;
    }
    event.preventDefault();
    setIsDisabled(true);
    setIsLoading(true);

    taskService
      .submitUserInput({
        inputData: {
          comment: true,
          recipes: []
        },
        text: "Give me the recipe that I am asking for",
        objective: recipeDescription
      })
      .then((returnedResponse) => {
        let parsed = JSON.parse(returnedResponse.text)
        addMessage({ sender: "ai", recipe: parsed.recipe, comment: parsed.comment})
        setIsLoading(false)
      })
      .catch((error) => {
        console.log(error)
      });
  };

  return (
    <>
      <div className='recipe-description-wrapper'>
        <form onSubmit={chooseRecipeDescription} className="recipe-description-input">
          <h3 style={{"maxWidth": "200px"}}>Which recipe do you need </h3>
          <input 
            type="text"
            disabled={isDisabled}
            placeholder="What recipe do you want"
            value={recipeDescription}
            onChange={(event) => setRecipeDescription(event.target.value)}
          />
          <button 
            type="button"
            disabled={isDisabled}
            className="recipe-description-submit-btn"
            onClick={chooseRecipeDescription}>
            Submit 
          </button>
        </form>
      </div>
    </>
  );
};

export default RecipeDescriptionForm;
