<template>
  <div ref="displayArea" class="flex flex-grow-1 flex-column align-content-between h-full">
    <div class="grid h-full">
      <Workspace
        ref="WorkspaceComponent"
        class="col-6"
        @submit="submitData"
        :inputData="currentInteraction.interactionData"
        :isLoading="currentInteraction.isLoading"
      />

      <div class="flex flex-column col-6">
        <ScrollPanel ref="chatpanel" :style="{ height: scrollpaneMax + 'px' }">
          <ConversationDisplay :conversation="currentInteraction.history"> </ConversationDisplay>
          <div class="grid">
            <div class="col-10">
              <Interaction
                ref="InteractionComponent"
                @submit="submitData"
                :inputData="currentInteraction.interactionData"
                :isLoading="currentInteraction.isLoading"
              />
            </div>
            <div class="col-2">
              <Button v-if="!showRatings" @click="() => (showRatings = true)" label="Finish" />
            </div>
          </div>
        </ScrollPanel>

        <Ratings v-if="showRatings" @ratingsSubmitted="() => (showRatings = false)" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import type { SubmissionData } from '@/stores/types'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { defineComponent, ref, nextTick } from 'vue'
import { useResizeObserver } from '@vueuse/core'

import Button from 'primevue/button'
import ScrollPanel from 'primevue/scrollpanel'

import ConversationDisplay from './ConversationDisplay.vue'
import Workspace from '@/tasks/Workspace.vue'
import Interaction from '@/tasks/Interaction.vue'
import Ratings from '@/components/Ratings.vue'

export default defineComponent({
  name: 'TaskInterface',
  components: {
    Workspace,
    ConversationDisplay,
    Interaction,
    Button,
    Ratings,
    ScrollPanel
  },
  data() {
    return {
      scrollpaneMax: 600,
      showRatings: false
    }
  },
  props: {
    inputData: {
      type: Object,
      required: false
    }
  },
  setup() {
    const taskStore = useTaskStore()
    const { currentInteraction, task } = storeToRefs(taskStore)
    const WorkspaceComponent = ref<InstanceType<typeof Workspace> | null>(null)
    const InteractionComponent = ref<InstanceType<typeof Interaction> | null>(null)
    return { taskStore, task, currentInteraction, InteractionComponent, WorkspaceComponent }
  },
  methods: {
    async scrollToBottom(): Promise<void> {
      console.log('scrolling to bottom')
      const scrollPaneRef = this.$refs.chatpanel as any //Ref<ScrollPanel>;
      const content = scrollPaneRef.$el.querySelector('.p-scrollpanel-content')
      if (!content) return
      // set the position of the scrollpane.
      content.scrollTop = content.scrollHeight
    },
    updateHeights() {
      const area = this.$refs.displayArea as HTMLElement
      const rightSideHeight = area == null ? 600 : area.offsetHeight
      console.log(`max scrollpane hight is ${rightSideHeight}`)
      //this.scrollpaneMax = rightSideHeight
    },
    async submitData() {
      console.log('Submitting data')
      let workspaceData = {} as SubmissionData
      if (this.WorkspaceComponent) {
        workspaceData = await this.WorkspaceComponent.getSubmissionData()
      }
      let interactionData = {} as SubmissionData
      if (this.InteractionComponent) {
        interactionData = this.InteractionComponent.getSubmissionData()
      }
      this.taskStore.submitUserInput(
        this.task.buildSubmissionObject(workspaceData, interactionData)
      )

      this.scrollToBottom()
    }
  },
  computed: {
    history_size(): number {
      return this.currentInteraction.history.length
    }
  },
  watch: {
    async history_size(newValue) {
      // doesn't matter yet, this could call code in the Godot game (if we have the option)
      await nextTick()
      this.scrollToBottom()
    }
  },
  mounted() {
    const rhs = this.$refs.displayArea as HTMLDivElement
    useResizeObserver(rhs, (entries: any) => {
      this.updateHeights()
    })
    this.updateHeights()
  }
})
</script>
