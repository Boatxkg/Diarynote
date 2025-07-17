import axios from 'axios'

export const registerUser = async (username, password) => {
  try {
    const res = await axios.post('http://localhost:5000/api/register', {
      username,
      password,
    })
    return res.data
  } catch (err) {
    console.error(err)
    throw err
  }
}
