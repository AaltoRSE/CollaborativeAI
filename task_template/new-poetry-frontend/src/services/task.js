import axios from 'axios'
// import type { SubmissionObject, Task, TaskInteraction, TaskSubmission } from './types'

const baseUrl = "/api/v1/task"

const submitUserInput = (newUserMessage) => {
  console.log(`new message submitted: ${JSON.stringify(newUserMessage)}`)
  const request = axios.post(`${baseUrl}/process`, newUserMessage)
  return request.then(response => response.data)
}

const finishTask = (rating) => {
  // const ratingjson = { metrics: { rating: rating } }
  // const request = 
  //   axios
  //     .post(`${baseUrl}/finish`, ratingjson)
  //     .then((response) => {
  //       console.log(`Rating ${rating} submitted`)
  //     })
  //     .catch((error) => {
  //       console.log(error)
  //     })
  // return request.then(response => response.data)
  console.log(`finish ${rating}`)
}

export default { 
  submitUserInput, 
  finishTask
}