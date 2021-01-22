<template>
  <div class='toast position-absolute mx-auto' role='alert' aria-live='assertive' aria-atomic='true' data-delay='2000'
    :class="{ 'bg-danger text-white': hasError }">
    <div class='toast-body'>{{ text }}</div>
  </div>
</template>

<script>
  export default {
    props: ['text', 'hasError'],
  };
</script>

<style scoped>
</style>