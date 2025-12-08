import { useState, useEffect } from "react";
import taskService from '../services/task'

const colors = ["#b71c1c", "#f44336", "#ff9800", "#ffeb3b", "#009688", "#81c784", "#4caf50"];

const FeedbackForm = ({ topic, messages }) => {
  const [ratingSubmitted, setRatingSubmitted] = useState(false);
  const [collaborationRating, setCollaborationRating] = useState(null);
  const [aiPerformanceRating, setAiPerformanceRating] = useState(null);
  const [clarityRating, setClarityRating] = useState(null);
  const [creativityRating, setCreativityRating] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [questionList, setQuestionList] = useState([]);

  const questions = [
    {
      id: "Collaboration metric",
      content: "The AI collaborated well with me",
      onSelected: setCollaborationRating,
    },
    {
      id: "Performance metric",
      content: "Overall, the AI's performance was high",
      onSelected: setAiPerformanceRating,
    },
    {
      id: "Clarity metric",
      content: "It was easy to understand what the AI does and what I am supposed to do",
      onSelected: setClarityRating,
    },
    {
      id: "Creativity metric",
      content: "The AI helped me become more creative",
      onSelected: setCreativityRating,
    },
  ]

  const getCorrespondingRating = (id) => {
    if (id == "Collaboration metric") {
      return collaborationRating;
    } else if (id == "Performance metric") {
      return aiPerformanceRating;
    } else if (id == "Clarity metric") {
      return clarityRating;
    } else {
      return creativityRating;
    }
  }

  const shuffleQuestionList = (questions) => {
    const temp = [...questions]
    let idx = temp.length
    while (idx != 0) {
      let randomIdx = Math.floor(Math.random() * idx);
      idx -= 1;
      [temp[idx], temp[randomIdx]] = [temp[randomIdx], temp[idx]];
    }
    return temp;
  }

  useEffect(() => {
    setQuestionList(shuffleQuestionList(questions));
  }, []);
  
  const handleMetricsSubmit = async () => {
    setRatingSubmitted(true);
    const modelName = await taskService.finishTask(      
      {
        "collaboration_metric": collaborationRating,
        "ai_performance_metric": aiPerformanceRating,
        "clarity_metric": clarityRating,
        "creativity_metric": creativityRating,
        "topic": topic,
        "message_log": messages
      }
    )
    setModelInfo(modelName["modelInfo"])
  }

  return (
    <div className="feedback-container">
      <h2>Please rate your experience based on the below metric</h2> <br></br>
      <div className="rating-container">
        {questionList.map(question => (
          <div key={question.id} className="collaboration-metric">
            <h3>"{question.content}"</h3>
            <div className="rating-selector">
              {[0, 1, 2, 3, 4, 5, 6].map(rating => (
                <div
                  key={rating}
                  className={`rating-circle ${rating + 1 === getCorrespondingRating(question.id) ? "selected" : ""}`}
                  style={{
                    "backgroundColor": colors[rating]
                  }}
                  onClick={() => {
                    question.onSelected(rating+1)
                  }}
                >
                  {rating + 1}
                </div>
              ))}
            </div>
            <br></br>
          </div>
        ))}
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
