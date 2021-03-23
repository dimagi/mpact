const clearStorage = () => {
  localStorage.removeItem('username');
  localStorage.removeItem('Token');
  localStorage.removeItem('refreshToken');
};
export {
  clearStorage,
};

