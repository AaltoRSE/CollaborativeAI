<template>
  <!-- the iframe is allowed to be maximised-->
</template>

<script lang="ts">
import { type PropType } from 'vue'
import type { SubmissionData } from '@/stores/types'

export default {
  name: 'WorkspaceComponent',
  components: {},
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
  emits: ['submit'], // submit will initialize the submission process
  setup(props) {},
  methods: {
    /**
     * Generate the image dtaa to be used in the submission
     * @@return the image data as a string
     */
    async getSubmissionData(): Promise<SubmissionData> {
      return {} as SubmissionData // "Not Implemented"
    }
  },
  watch: {
    async inputData(newValue) {
      // handle updated input data (i.e. the latest submission change)
    }
  },
  mounted() {}
}
</script>
