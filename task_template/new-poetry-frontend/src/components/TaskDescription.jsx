const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Poetry task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>The user chooses a theme for the poem.</li>
        <li>After that, the AI will ask what tone should be set for the poem and for what disability the user wants to be inclusive</li>
        <li>The user and AI take turns to write the poem. The AI will always ask for user's feedback before including its line in the poem.</li>
        <li>There are two input field: the first one is for adding a new poemline, the second one is for sending the model a comment</li>
        <li>The poem is finished when it reaches the 9-line limit</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
