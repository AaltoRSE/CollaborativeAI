<template>
  <!-- the iframe is allowed to be maximised-->
  <iframe
    width="1000px"
    height="562px"
    ref="iframe"
    frameborder="0"
    allowfullscreen="true"
    id="game_drop"
    allowtransparency="true"
    allow="autoplay; fullscreen *; geolocation; microphone; camera; midi; monetization; xr-spatial-tracking; gamepad; gyroscope; accelerometer; xr; cross-origin-isolated"
    mozallowfullscreen="true"
    msallowfullscreen="true"
    scrolling="no"
    webkitallowfullscreen="true"
  />
</template>

<script lang="ts">
import { ref, type PropType, nextTick } from 'vue'
import type { SubmissionData } from '@/stores/types'
import InputField from '@/components/InputField.vue'
import html2canvas from 'html2canvas'

export default {
  name: 'TangramComponent',
  components: { InputField },
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
  emits: ['submit', 'updateHistory'],
  setup(props) {
    const iframe = ref<HTMLIFrameElement | null>(null)
    return {
      iframe
    }
  },
  methods: {
    /**
     * This method is used by the game to submit the data to the task
     */

    async getSubmissionData(): Promise<SubmissionData> {
      console.log('Calling submit Data!')
      const submissionData = {} as SubmissionData

      // take a screenshot of the game
      if (this.iframe && this.iframe.contentDocument) {
        const canvas = await html2canvas(this.iframe.contentDocument.body)
        const imgData = canvas.toDataURL()
        submissionData.image = imgData
      }
      submissionData.data = {}
      submissionData.text = ''
      return submissionData
    }
  },
  watch: {
    async inputData(newValue) {
      // doesn't matter yet, this could call code in the Godot game (if we have the option)
    }
  },
  mounted() {
    if (this.iframe) {
      console.log('There is an iframe')
      const iframeContent = this.iframe.contentWindow as any
      this.iframe.src = '/godot_games/tangram/tangram.html'
      nextTick()
      console.log(iframeContent.taskLoaded)
    }
  }
}
</script>
