<template>
  <div>
    Welcome to Dimagi Telegram Bot!
    <Test />
    <router-view></router-view>
  </div>
</template>

<script>
import Test from "./components/Test.vue";
export default {
  components: {
    Test: Test,
  },
};
</script>