<template>
  <div class="grid w-full">
    <div class="col-11">
      <div class="flex flex-column p-input-icon-right w-full flex-grow-1">
        <div class="flex flex-row w-full mb-2">
          <div class="flex flex-shrink-0 w-8 mr-3">
            <TextArea
              v-if="allowText"
              :disabled="isLoading"
              class="w-full"
              ref="queryInput"
              @keydown="checkSubmit"
              autoResize
              rows="1"
              v-model="queryText"
              id="input"
              type="text"
            />
          </div>
          <div ref="submitDiv" class="flex flex-1 flex-grow-1 overflow-x-hidden">
            <Button icon="pi pi-send" :disabled="isLoading" @click="sendRequest" label="Submit" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// Input field for chats.

import { nextTick } from 'vue'
import { storeToRefs } from 'pinia'

import TextArea from 'primevue/textarea'
import Button from 'primevue/button'

export default {
  components: { TextArea, Button },
  props: {
    inputText: {
      type: String,
      required: true
    },
    isLoading: {
      type: Boolean,
      required: true
    },
    allowText: {
      type: Boolean,
      required: true
    }
  },
  emits: ['submit', 'update:inputText'],
  methods: {
    sendRequest(event: KeyboardEvent | MouseEvent) {
      event.preventDefault()
      this.$emit('submit')
    },
    checkSubmit(event: KeyboardEvent) {
      if (event.key === 'Enter' && !event.shiftKey) {
        this.sendRequest(event)
      }
    }
  },
  setup() {},
  computed: {
    queryText: {
      get(): string {
        return this.inputText
      },
      set(newText: string) {
        this.$emit('update:inputText', newText)
      }
    }
  },
  mounted() {}

  // triggered either when clicking on the icon, or pressing enter in the prompt field
}
</script>
