<template>
  <div class="flex flex-column ml-3 p-input-icon-right w-full">
    <div class="flex flex-row w-full mb-2">
      <div class="flex flex-shrink-0 w-10 mr-3">
        <TextArea
          :disabled="isLoading"
          class="w-full"
          ref="queryInput"
          @keydown="checkSubmit"
          autoResize
          rows="1"
          v-model="inputText"
          id="input"
          type="text"
        />
      </div>
      <div ref="submitDiv" class="flex flex-1 flex-grow-1 overflow-x-hidden">
        <Button icon="pi pi-send" :disabled="isLoading" @click="sendRequest" label="Submit" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { type PropType } from 'vue'
import type { SubmissionData } from '@/stores/types'
import TextArea from 'primevue/textarea'
import Button from 'primevue/button'

export default {
  name: 'InteractionComponent',
  components: { TextArea, Button },
  props: {
    inputData: {
      type: Object as PropType<SubmissionData>,
      required: false
    },
    isLoading: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      inputText: ''
    }
  },
  emits: ['submit'], // submit will initialize the submission process
  setup(props) {},
  methods: {
    /**
     * Generate the image data to be used in the submission
     * @@return the image data as a string
     */
    getSubmissionData(): SubmissionData {
      return { text: this.inputText } as SubmissionData
    },
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
  watch: {
    async inputData(newValue) {
      // handle updated input data (i.e. the latest submission change)
    },
    isLoading(newValue) {
      // if no longer loading reset the text
      if (!newValue) {
        this.inputText = ''
      }
    }
  },
  mounted() {}
}
</script>
