const TaskDescription = () => {
  return (
    <div className="task-description">
      <h2>🖋️ Code tutor task</h2>
      <h3>📜 Rules</h3>
      <ol>
        <li>Provide the description of the topic/problem</li>
        <li>The code blocks are written in Markdown. Quick tutorial <a target="_blank" href="https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks" style={{"color": "red"}}>here</a></li>
        <li>The AI then iteratively guide you through the topic/problem.</li>
        <li>If you want to discuss with the AI, you can do that in the Conversation box.</li>
        <li>When you are sastified with the result. Please then rate your experience with the AI.</li>
      </ol>
    </div>
  );
};

export default TaskDescription;
