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
        return axios
          .post(`${baseURL}/token/refresh/`, {
            refresh: `${localStorage.getItem('refreshToken')}`,
          })
          .then(async (res) => {
            localStorage.setItem('Token', res.data.access);
            return new Promise(async (resolve, reject) => {
              const axiosErr = await axios.request(err.config)
              resolve(axiosErr);
            });
          })
          .catch((err) => {
            return new Promise((resolve, reject) => {
              clearStorage();
              router.push('/login').catch((err)=>{console.log(err);});
              reject(err);
            });
          });
      } else {
        clearStorage();
        router.push('/login').catch((err)=>{console.log(err);});
      }
    }
    return Promise.reject(err);
  },
);

// allow blob requests to return JSON when they fail
// https://github.com/axios/axios/issues/815#issuecomment-453963910
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (
      error.request.responseType === 'blob' &&
      error.response.data instanceof Blob &&
      error.response.data.type &&
      error.response.data.type.toLowerCase().indexOf('json') != -1
    ) {
      return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.onload = () => {
          error.response.data = JSON.parse(reader.result);
          resolve(Promise.reject(error));
        };
        reader.onerror = () => {
          reject(error);
        };
        reader.readAsText(error.response.data);
      });
    }
    return Promise.reject(error);
  }
);

export default axios;
