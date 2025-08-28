const DialogueItem = ({ message, style }) => {
  const messageClass = message.sender === "user" ? "user-dialogue" : "ai-dialogue";

  const parsedJSON = message.recipe
  
  return (
    <>
      <div className={`dialogue-poem ${messageClass}`}>
        <b>Recipe name: </b>{parsedJSON.name} <br></br><br></br>
        <b>Ingredients: </b> <br></br>
        <ol>
          {Object.entries(parsedJSON.ingredients).map(([key, value]) => (
            <li key={key}>{key}: {value}</li>
          ))}
        </ol>
        <br></br>
        <b>Instruction: </b> <br></br>
        <ol>
          {Object.entries(parsedJSON.instruction).map(([key, step]) => (
            <li key={key}>{step}</li>
          ))}
        </ol>
        <br></br>
        <b>Number of serving: </b>{parsedJSON.servings} <br></br>
        <b>Prep time: </b>{parsedJSON.prep_time}. <br></br>
        <b>Cook time: </b>{parsedJSON.cook_time}. <br></br>
        <b>Total time: </b> {parsedJSON.total_time}. <br></br>
        <br></br>
      </div>
    </>
  );
};

export default DialogueItem;
