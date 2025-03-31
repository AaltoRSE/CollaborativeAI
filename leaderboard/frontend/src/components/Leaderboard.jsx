import React, { useState, useEffect } from 'react';
import ratingServices from '../services/ratings';
import '../index.css';

const task_list = ["tangram_task", "poetry_task", "mealplan"]

const Leaderboard = () => {
  const [leaderboardData, setLeaderboardData] = useState({
    overall: [],
    tangram_task: [],
    poetry_task: [],
    mealplan: []
  });
  const [entryCount, setEntryCount] = useState(0)
  const [modelCount, setModelCount] = useState(0)

  useEffect(() => {
    fetchData();
  }, []);

  const calculateAverageRating = (ratingObj, leaderboardName) => {
    const averageRatingData = Object.keys(ratingObj).map((model) => ({
      model,
      rating: ratingObj[model].ratingSum / ratingObj[model].count,
    }));
    averageRatingData.sort((a, b) => b.rating - a.rating);
    setLeaderboardData((prev) => ({ ...prev, [leaderboardName]: averageRatingData }));
  }

  const fetchData = async () => {
    const entryList = await ratingServices.getAllRatings()
    // const entryList = [
    //   {
    //     "task_name":"mealplan",
    //     "model":"A",
    //     "collaboration_metric":5
    //   },
    //   {
    //     "task_name":"mealplan",
    //     "model":"B",
    //     "collaboration_metric":6
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"B",
    //     "collaboration_metric":6
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"B",
    //     "collaboration_metric":5
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"C",
    //     "collaboration_metric":3
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"C",
    //     "collaboration_metric":2
    //   },
    //   {
    //     "task_name":"mealplan",
    //     "model":"A",
    //     "collaboration_metric":4
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"A",
    //     "collaboration_metric":6
    //   },
    //   {
    //     "task_name":"poetry_task",
    //     "model":"A",
    //     "collaboration_metric":2
    //   },
    //   {
    //     "task_name":"tangram_task",
    //     "model":"B",
    //     "collaboration_metric":6
    //   },
    //   {
    //     "task_name":"tangram_task",
    //     "model":"A",
    //     "collaboration_metric":2
    //   },
    // ]
    setEntryCount(entryList.length)
    setModelCount(new Set(entryList.map((entry) => entry.model)).size)

    //Extract data into different task categories
    const extractedData = {}
    task_list.forEach((task) => extractedData[task] = [])
    entryList.forEach((entry) => {
      const category = entry.task_name
      const model = entry.model 
      const rating = entry.rating ?? entry.collaboration_metric
      extractedData[category].push({ model, rating})
    })

    const overallData = {};
    const taskData = {};

    //loop through extracted data to fill overall data
    task_list.forEach((task) => {
      extractedData[task].forEach((entry) => {
        if (!overallData[entry.model]) {
          overallData[entry.model] = { ratingSum: 0, count: 0 };
        }
        overallData[entry.model].ratingSum += entry.rating;
        overallData[entry.model].count++;
      });
    })

    //loop through extracted data to fill task data
    task_list.forEach((task) => {
      taskData[task] = {}
      extractedData[task].forEach((entry) => {
        if (!taskData[task][entry.model]) {
          taskData[task][entry.model] = { ratingSum: 0, count: 0 }
        }
        taskData[task][entry.model].ratingSum += entry.rating;
        taskData[task][entry.model].count++;
      });
    })
    calculateAverageRating(overallData, "overall")
    task_list.forEach(task => calculateAverageRating(taskData[task], task))
  };

  return (
    <div className="page-wrapper">
      <div className="title-wrapper">
        <h1 className="title">Leaderboard</h1>
      </div>
      <div className="content-wrapper">
        <div className="boxes-wrapper">
          <div className="info-box">
            <p>Number of Entries: {entryCount}</p>
            <p>Model Count: {modelCount}</p>
          </div>
        </div>
        <div className="overall-table">
          <h3>Overall</h3>
          <table>
            <thead>
              <tr className="overall-header">
                <th>Rank</th>
                <th>Model</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboardData["overall"].map((entry, index) => (
                <tr key={`${index}-${entry.model}`}>
                  <td>{index + 1}</td>
                  <td>{entry.model}</td>
                  <td>{entry.rating.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {task_list.map((category) => (
          <div key={category} className="leaderboard-table">
            <h3>
            {
              (() => {
                switch (category) {
                  case 'tangram_task':
                    return 'Tangram';
                  case 'poetry_task':
                    return 'Poetry';
                  case 'mealplan':
                    return 'Meal plan';
                  default:
                    return 'Placeholder'
                }
              })()
            }
            </h3>
            <table>
              <thead>
                <tr className="task-header">
                  <th>Rank</th>
                  <th>Model</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {leaderboardData[category].map((entry, index) => (
                  <tr key={`${index}-${entry.model}`}>
                    <td>{index + 1}</td>
                    <td>{entry.model}</td>
                    <td>{entry.rating.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
  
};



export default Leaderboard;
