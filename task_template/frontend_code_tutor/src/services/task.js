import axios from 'axios'

const baseUrl = "/api/v1/task"

const submitUserInput = (newUserMessage) => {
  const request = axios.post(`${baseUrl}/process`, newUserMessage)
  return request.then(response => response.data)
}

const finishTask = (rating) => {
  const ratingjson = {
    metrics: {
      rating: rating, 
      task_name: "code_tutor"
    }
  }
  const request = axios.post(`${baseUrl}/finish`, ratingjson)
  return request.then(response => response.data)
}

export default { 
  submitUserInput,
  finishTask,
}