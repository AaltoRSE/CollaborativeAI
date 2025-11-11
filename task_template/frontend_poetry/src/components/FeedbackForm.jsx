import { useState } from "react";
import taskService from '../services/task'

const colors = ["#b71c1c", "#f44336", "#ff9800", "#ffeb3b", "#009688", "#81c784", "#4caf50"];

const FeedbackForm = ({ }) => {
  const [ratingSubmitted, setRatingSubmitted] = useState(false);
  const [collaborationRating, setCollaborationRating] = useState(null);
  const [aiPerformanceRating, setAiPerformanceRating] = useState(null);
  const [clarityRating, setClarityRating] = useState(null);
  const [creativityRating, setCreativityRating] = useState(null);
  const [modelInfo, setModelInfo] = useState(null)

  const handleMetricsSubmit = async () => {
    setRatingSubmitted(true);
    const modelName = await taskService.finishTask(      
      {
        "collaboration_metric": collaborationRating,
        "ai_performance_metric": aiPerformanceRating,
        "clarity_metric": clarityRating,
        "creativity_metric": creativityRating
      }
    )
    setModelInfo(modelName["modelInfo"])
  }

  return (
    <div className="feedback-container">
      <h2>Please rate your experience based on the below metric</h2> <br></br>
      <div className="rating-container">
        <div className="collaboration-metric">
          <h3>"The AI collaborated well with me"</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === collaborationRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setCollaborationRating(rating+1)
                }}
              >
                {rating + 1}
              </div>
            ))}
          </div>
        </div>
        <br></br>
        <div className="ai-performance-metric">
          <h3>"Overall, the AI's performance was high"</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === aiPerformanceRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setAiPerformanceRating(rating+1)
                }}
              >
                {rating + 1}
              </div>
            ))}
          </div>
        </div>
        <br></br>
        <div className="coordination-metric">
          <h3>"It was easy to understand what the AI does and what I am supposed to do"</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === clarityRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setClarityRating(rating+1)
                }}
              >
                {rating + 1}
              </div>
            ))}
          </div>
        </div>
        <br></br>
        <div className="with-or-without-metric">
          <h3>"The AI helped me become more creative"</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === creativityRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setCreativityRating(rating+1)
                }}
              >
                {rating + 1}
              </div>
            ))}
          </div>
        </div>
      </div>
      {ratingSubmitted 
        ? <div className="after-rating-submitted">
            <h4>Thank you! The model that you worked with was {modelInfo}</h4>
            <button type="submit" className="reset-button" onClick={() => window.location.reload()}> Restart </button>
          </div>
        : <div>
            <button type="submit" className="submit-button" onClick={() => handleMetricsSubmit()}> Submit </button>
          </div>
      }
    </div>
  );
};

export default FeedbackForm;
