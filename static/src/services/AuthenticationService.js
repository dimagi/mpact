import Api from './Api';

export default {
  async addNewMessage({
    formattedPhoneNumber,
    otpNumber,
    phoneCodeHash,
    twoFactorAuthCode
  }) {
    try {
      const result = await Api.post('/login', {
        phone: formattedPhoneNumber,
        code: otpNumber,
        phone_code_hash: phoneCodeHash,
        password: twoFactorAuthCode,
      });
      return result;
    } catch (err) {
      console.error(err);
    }
  }
}