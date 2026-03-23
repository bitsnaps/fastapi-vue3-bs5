import axios from 'axios'

const api = axios.create({
  baseURL: `http://127.0.0.1:8000`,
  withCredentials: true, // This is the default
  headers: {
    'Access-Control-Allow-Origin': '*', 
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  timeout: 10000
})

export default {
  getCompletion(prompt: string) {

    // return fetch('http://127.0.0.1:8000/chat',{ 
    //     method: 'POST',
    return fetch('http://127.0.0.1:8000/',{ 
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
          },
        // body: JSON.stringify({"prompt": prompt}),
        credentials: 'include' // for google's IDX only.
    })
    // return api.post('/chat', prompt)
  }
}
