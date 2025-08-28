const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Math tutor task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Provide the description of the topic/problem.</li>
        <li>The math expressions are written in Markdown. Quick tutorial <a target="_blank" href="https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions" style={{"color": "red"}}>here</a></li>
        <li>The AI then iteratively guide you through the topic/problem.</li>
        <li>When you are sastified with the result. Please then rate your experience with the AI.</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
