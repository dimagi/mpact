<template>
  <div :class="['toast', 'position-absolute', 'mx-auto', { 'bg-danger text-white': hasError }]" aria-live='assertive'
    aria-atomic='true' role='alert' data-delay='2000'>
    <div class='toast-body text-center'>{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: 'toast',
  props: ['text', 'hasError'],
};
</script>
<style scoped>
.toast {
  left: 0;
  right: 0;
  z-index: 9999;
}
</style>
