import Axios from 'axios';
import router from '../router/index';

const baseURL = `${window.location.origin}/api`;

const axios = Axios.create({
  baseURL,
});

axios.interceptors.request.use(
  (config) => {
    const Token = localStorage.getItem('Token');
    const newConfig = config;
    newConfig.headers = {
      Token,
    };
    return newConfig;
  }, (err) => Promise.reject(err),
);

axios.interceptors.response.use((res) => res, (err) => {
  if (err.response.status === 401 || err.response.status === 403) {
    router.push('/login');
  }
  return Promise.reject(err);
});

export default axios;
