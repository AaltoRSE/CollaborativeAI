import axios from 'axios'

const baseUrl = "/api/v1"

const getAllRatings = async () => {
  const response = await axios.get(`${baseUrl}/rating`);
  return response.data
}

export default { 
  getAllRatings
}