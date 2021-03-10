import Axios from 'axios';
import router from '../router/index';
import { clearStorage } from '../utils/helpers';
const baseURL = `${window.location.origin}/api`;

const axios = Axios.create({
  baseURL,
});

axios.interceptors.request.use(
  (config) => {
    const Token = localStorage.getItem('Token');
    const newConfig = config;
    newConfig.headers = {
      Authorization: `Bearer ${Token}`,
    };
    return newConfig;
  },
  (err) => Promise.reject(err),
);

axios.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response.config.url == `${baseURL}/token/refresh/`) {
      clearStorage();
      router.push('/login');
      return new Promise((resolve, reject) => {
        reject(err);
      });
    }

    if (err.response.status === 401 || err.response.status === 403) {
      if (err.response.data.code === 'token_not_valid' && localStorage.getItem('Token')) {
        axios
          .post(`${baseURL}/token/refresh/`, {
            refresh: `${localStorage.getItem('refreshToken')}`,
          })
          .then((res) => {
            localStorage.setItem('Token', res.data.access);
            location.reload();
            return new Promise((resolve, reject) => {
              resolve(res);
            });
          })
          .catch((err) => {
            return new Promise((resolve, reject) => {
              clearStorage();
              router.push('/login');
              reject(err);
            });
          });
      } else {
        clearStorage();
        router.push('/login');
      }
    }
    return Promise.reject(err);
  },
);

export default axios;
