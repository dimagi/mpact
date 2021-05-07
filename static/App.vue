<template>
    <div class='app'>
        <error-boundary>
            <router-view></router-view>
        </error-boundary>
    </div>
</template>

<script>
import Vue from 'vue';
import VueMyToasts from 'vue-my-toasts'
import BootstrapComponent from 'vue-my-toasts/src/components/toasts/BootstrapComponent.vue'
import 'vue-my-toasts/dist/vue-my-toasts.css'

Vue.use(VueMyToasts, {
  component: BootstrapComponent,
  options: {
    width: '400px',
    position: 'top-middle',
  }
});

Vue.component('error-boundary', {
  template: '<div><slot></slot></div>',
  errorCaptured: (err, vm, info) => {
    console.error(err, vm, info);
    console.error('Something went wrong');
    return false;
  },
});

export default {
};
</script>

<style>
  @import url('./src/styles/index.css');
</style>
