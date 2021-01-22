<template>
  <div class='about-shown width-404  bg-white border-0 position-relative'>
    <div>
      <h3>
        <span class='about-text'>About</span><a @click='closeInfoComponent()'
          class='hide-btn cursor-pointer position-absolute'>&times;</a>
      </h3>
      <p class='telegram-text'>
        The mpact-Telegram web-client is a free, fast and secure way to enjoy most of
        <strong>Telegram</strong>'s features right in your
        <strong>web-browser</strong>.
      </p>
      <p class='telegram-text'>
        It is always synced with the <strong>Telegram app</strong> on your
        mobile device, which makes it a perfect tool for messaging and file
        sharing.
      </p>
      <div class='telegram-text'>
        Our
        <a href='https://github.com/zhukov/webogram' target='_blank'>source code</a>
        is open, so everyone can make a contribution.
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ['receiveClass'],
    methods: {
      closeInfoComponent() {
        this.$emit('closeInfoComponent');
      },
    },
  };
</script>
<style scoped>
  .about-shown {
    padding: 44px 65px;
    -webkit-box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2),
      1px 0 0 rgba(97, 127, 152, 0.1), -1px 0 0 rgba(97, 127, 152, 0.1);
    -moz-box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2),
      1px 0 0 rgba(97, 127, 152, 0.1), -1px 0 0 rgba(97, 127, 152, 0.1);
    box-shadow: 0 1px 1px rgba(97, 127, 152, 0.2), 1px 0 0 rgba(97, 127, 152, 0.1),
      -1px 0 0 rgba(97, 127, 152, 0.1);
    border-radius: 2px;
    max-width: none;
  }

  .about-shown .about-text {
    font-size: 15px;
    font-weight: 700;
    text-align: left;
    color: #222;
  }

  .about-shown .hide-btn {
    font-size: 15px;
    font-weight: 700;
    text-align: left;
    color: #999;
    margin-left: 10px;
    right: 10px;
    top: 10px;
  }

  .about-shown .telegram-text {
    font-size: 13px;
    line-height: 160%;
  }
</style>