const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Meal plan task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Provide your meal plan description.</li>
        <li>The AI then gives you a recommended meal plan.</li>
        <li>If you want to discuss with the AI about the meal plan, you can do that in the Conversation box.</li>
        <li>When satisfied with the result, click "Finish" to rate your experience.</li>
        <li><strong>Notice: </strong>your prolific ID and input to the AI will be stored in this study</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
