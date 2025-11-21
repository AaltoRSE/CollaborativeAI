const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Recipe plan task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Provide the name of the recipe.</li>
        <li>The AI then gives you a recommended recipe.</li>
        <li>If you want to discuss with the AI about the recipe, you can do that in the Conversation box.</li>
        <li>When satisfied with the result, click "Finish" to rate your experience.</li>
        <li>Notice: your input to the AI will be stored in this study</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
