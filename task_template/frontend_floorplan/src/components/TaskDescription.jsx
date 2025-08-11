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
        <li>If you want to discuss with the AI about the floor plan, you can do that in the Conversation box</li>
        <li>When you are sastified with the floor plan. Please then rate your experience with the AI</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
