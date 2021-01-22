import Axios from 'axios';
import router from '../router/index';

const baseURL = `${location.origin}/api`;
const axios = Axios.create({
  baseURL,
});

axios.interceptors.request.use(
  config => {
    const Token = localStorage.getItem('Token');
    config.headers = {
      Token,
    }
    return config;
  }, err => {
    return Promise.reject(err)
  })

axios.interceptors.response.use(res => {
  return res;
}, err => {
  if (err.response.status === 401 || err.response.status === 403) {
    router.push('/login');
  }
  return Promise.reject(err)
})

export default axios;