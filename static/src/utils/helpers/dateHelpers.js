const convertDate = (date) => {
  const dateString = new Date(date);
  let month = `${dateString.getMonth() + 1}`;
  let day = `${dateString.getDate()}`;
  const year = dateString.getFullYear();
  if (month.length < 2) month = `0${month}`;
  if (day.length < 2) day = `0${day}`;
  return [ year, month, day].join('-');
}

const convertTime = (time) => {
  const timeString = new Date(time);
  return `${timeString.getHours().toString().padStart(2,'0')}:${timeString.getMinutes().toString().padStart(2,'0')}`;
}

const convertDateTime = (inputDate) => {
  return convertDate(inputDate) + ' ' + convertTime(inputDate)
}

export default {
  convertDate,
  convertTime,
  convertDateTime,
}