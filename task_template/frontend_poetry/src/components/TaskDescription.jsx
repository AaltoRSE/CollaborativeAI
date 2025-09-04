const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Poetry task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Provide a theme for the poem.</li>
        <li>The AI then writes the first line.</li>
        <li>Then it is your turn to write.</li>
        <li>If you want to discuss with the AI, you can do that in the Dialogue box.</li>
        <li>The game ends when the poem has 9 lines.</li>
        <li>When satisfied with the result, click "Finish" to rate your experience.</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
