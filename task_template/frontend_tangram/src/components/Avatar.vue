<template>
  <div class="flex avatarcontainer">
    <div
      class="flex avatar justify-content-center align-items-center flex-column"
      :class="isGPT ? 'gpt' : 'user'"
    >
      <!--<i class="pi pi-server"></i>-->
      {{ ID }}
      <i v-if="!isGPT" class="pi pi-user user"></i>
      <i v-else class="pi pi-server gpt"></i>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  props: {
    isGPT: {
      type: Boolean,
      required: true
    },
    ID: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.user {
  border-color: black;
  background-color: black;
  color: white;
}

.gpt {
  border-color: darkcyan;
  background-color: darkcyan;
  color: black;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.avatarcontainer {
  min-width: 50px;
  padding: 10px;
}
</style>
