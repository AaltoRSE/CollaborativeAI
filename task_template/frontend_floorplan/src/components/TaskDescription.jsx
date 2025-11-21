const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Floor planner task</h2>
      <h3>📜 Rules</h3>
      <ol>
        {/* <li>Provide the description of the room.</li> */}
        <li>You are designing a bedroom with the AI</li>
        {/* <li>The AI then gives you an initial floor plan.</li>
        <li>If you want to discuss with the AI about the floor plan, you can do that in the Conversation box.</li>
        <li>When you are sastified with the floor plan. Please then rate your experience with the AI.</li> */}
        <li>The AI gives instructions on how to place the next piece</li>
        <li>You make the first move then the AI plays its move</li>
        <li>To rotate or delete a piece from the grid, right click on that piece to open a drop-down menu and then select the option</li>
        <li>For macOS trackpad users, ensure the "Secondary click" option inside the Trackpad setting is not set to "Off". Use the set option there to open the drop-down menu for rotating and removing pieces.</li>
        <li>If you want to discuss with the AI about the floor plan, you can do that in the Conversation box</li>
        <li>When satisfied with the result, click "Finish" to rate your experience.</li>
        <li>Notice: your input to the AI will be stored in this study</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
