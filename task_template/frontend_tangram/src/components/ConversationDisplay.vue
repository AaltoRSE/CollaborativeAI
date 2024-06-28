<script setup lang="ts">
import Message from 'primevue/message'
import { computed } from 'vue'
import ConversationItem from './ConversationItem.vue'
import ProgressSpinner from 'primevue/progressspinner'

import type { DisplayMessage } from '@/stores/types'
import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'

const props = defineProps({
  conversation: { type: Array<DisplayMessage>, required: true },
  userInitials: { type: String, default: 'You' },
  modelName: { type: String, default: 'AI' }
})
const emit = defineEmits(['messagesUpdated', 'askQuestion'])
const taskStore = useTaskStore()
const { currentInteraction, lastInteraction } = storeToRefs(taskStore)

const errored = computed(() => {
  if (props.conversation) {
    const convExists = props.conversation.at(-1)
    if (convExists) {
      return convExists.error
    } else {
      return false
    }
  } else {
    return false
  }
})
</script>

<template>
  <div class="chat-container">
    <ConversationItem
      v-for="(message, index) in conversation"
      class="flex m-1 message"
      :message="message"
      :userName="userInitials"
      :modelName="modelName"
      :key="index"
    >
    </ConversationItem>
    <Message v-if="errored" severity="error"
      >Latest response from AI could not be interpreted</Message
    >
    <div v-if="currentInteraction.isLoading" class="flex justify-center">
      <ProgressSpinner v-if="currentInteraction.isLoading" />
      AI Calculating...
    </div>
  </div>
</template>
<style scoped>
.message {
  margin-bottom: 10px;
}
.chat-container {
  width: 100%;
  padding: 3rem;
}
</style>
