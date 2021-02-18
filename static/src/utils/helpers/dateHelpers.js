const convertDate = (date) => {
  const dateString = new Date(date);
  let month = `${dateString.getMonth() + 1}`;
  let day = `${dateString.getDate()}`;
  const year = dateString.getFullYear();
  if (month.length < 2) month = `0${month}`;
  if (day.length < 2) day = `0${day}`;
  return [day, month, year].join('-');
}

const convertTime = (time) => {
  const timeString = new Date(time);
  return `${timeString.getHours()}:${timeString.getMinutes()}`;
}

export {
  convertDate,
  convertTime,
}

export default {
  convertDate,
  convertTime,
}