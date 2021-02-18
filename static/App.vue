<template>
    <div class='app'>
        <error-boundary>
            <router-view></router-view>
        </error-boundary>
    </div>
</template>

<script>
import Vue from 'vue';

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
