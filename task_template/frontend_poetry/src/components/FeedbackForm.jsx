import { useState, useEffect } from "react";
import taskService from '../services/task'
import axios from 'axios'

const colors = ["#b71c1c", "#f44336", "#ff9800", "#ffeb3b", "#009688", "#81c784", "#4caf50"];

const FeedbackForm = ({ }) => {
  const [ratingSubmitted, setRatingSubmitted] = useState(false);
  const [collaborationRating, setCollaborationRating] = useState(null);
  const [aiPerformanceRating, setAiPerformanceRating] = useState(null);
  const [coordinationRating, setCoordinationRating] = useState(null);
  const [efficiencyRating, setEfficiencyRating] = useState(null);
  const [modelInfo, setModelInfo] = useState('')

  useEffect(() => {
    const handleReconnect = () => {
      const offlineRating = localStorage.getItem('offline-rating');
      console.log(offlineRating)
      console.log(JSON.parse(offlineRating))
      if (offlineRating) {
        // alert('Offline rating submitted!');
        // localStorage.removeItem('offline-rating');
        const ratingjson = {
          metrics: {
            rating: JSON.parse(offlineRating), 
            task_name: "poetry_task"
          }
        }
        axios.post('/api/v1/task/finish', ratingjson)
          .then(() => {
            alert('Offline rating submitted!');
            localStorage.removeItem('offline-rating');
          })
          .catch((e) => {
            console.error('Failed to send offline rating', e);
          });
      }
    };

    // Run once in case user is already online with stored data
    handleReconnect();

    // Also run when they reconnect later
    window.addEventListener('online', handleReconnect);
    return () => {
      window.removeEventListener('online', handleReconnect);
    };
  }, []);

  const handleMetricsSubmit = async () => {
    const ratingJson = {
      "collaboration_metric": collaborationRating,
      "ai_performance_metric": aiPerformanceRating,
      "coordination_metric": coordinationRating,
      "efficiency_metric": efficiencyRating
    }
    if (navigator.onLine) {
      setRatingSubmitted(true);
      const modelName = await taskService.finishTask(ratingJson)
      setModelInfo(modelName["modelInfo"])
    } else {
      localStorage.setItem('offline-rating', JSON.stringify(ratingJson));
      alert('You are currently offline. The rating will be sent after you reconnect.');
    }
  }

  return (
    <div className="feedback-container">
      <h2>Please rate your experience based on the below metric</h2> <br></br>
      <div className="rating-container">
        <div className="collaboration-metric">
          <h3>"We collaborated well with the AI."</h3>
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
          <h3>"The AI performed well."</h3>
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
          <h3>"We succesfully coordinated our strategy to write a good poem."</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === coordinationRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setCoordinationRating(rating+1)
                }}
              >
                {rating + 1}
              </div>
            ))}
          </div>
        </div>
        <br></br>
        <div className="with-or-without-metric">
          <h3>"Working with the AI was more efficient than working alone."</h3>
          <div className="rating-selector">
            {[0, 1, 2, 3, 4, 5, 6].map(rating => (
              <div
                key={rating}
                className={`rating-circle ${rating + 1 === efficiencyRating ? "selected" : ""}`}
                style={{
                  "backgroundColor": colors[rating]
                }}
                onClick={() => {
                  setEfficiencyRating(rating+1)
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
