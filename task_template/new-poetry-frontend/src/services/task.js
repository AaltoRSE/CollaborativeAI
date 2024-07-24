import axios from 'axios'

const baseUrl = "/api/v1/task"

const submitUserInput = (newUserMessage) => {
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