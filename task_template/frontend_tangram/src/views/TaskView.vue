<template>
  <div class="flex flex-column align-content-between h-screen">
    <div class="taskview-header">
      <h1>{{ task.title }}</h1>
      <p>{{ task.description }}</p>
      <div v-if="currentInteraction.objective">
        The current Objective is: {{ currentInteraction.objective }}
      </div>
      <InputField
        v-else
        v-model:inputText="taskObjective"
        :isLoading="false"
        :allowText="true"
        @submit="finishedObjective()"
      />
    </div>

    <div v-if="currentInteraction.objective">
      <TaskInterface
        v-show="!currentInteraction.isLoading"
        :task-component="task.id"
        :input-data="lastInteraction"
      ></TaskInterface>
    </div>
  </div>
</template>

<script lang="ts">
import ScrollPanel from 'primevue/scrollpanel'
import Button from 'primevue/button'
import ConversationDisplay from '@/components/ConversationDisplay.vue'
import InputField from '@/components/InputField.vue'
import TaskInterface from '@/components/TaskInterface.vue'
import Ratings from '@/components/Ratings.vue'

import { defineComponent } from 'vue'

import { useTaskStore } from '@/stores'
import { storeToRefs } from 'pinia'
import { useResizeObserver } from '@vueuse/core'
import ProgressSpinner from 'primevue/progressspinner'

export default defineComponent({
  name: 'TaskView',
  components: {
    Button,
    ConversationDisplay,
    ScrollPanel,
    InputField,
    TaskInterface,
    ProgressSpinner,
    Ratings
  },
  data() {
    return {
      taskObjective: '',
      scrollpaneMax: 300,
      showRatings: false
    }
  },
  setup() {
    const taskStore = useTaskStore()
    const { task, currentInteraction, lastInteraction } = storeToRefs(taskStore)
    return { task, currentInteraction, lastInteraction, taskStore }
  },
  methods: {
    finishedObjective() {
      this.taskStore.startTask()
      this.taskStore.setObjective(this.taskObjective)
      console.log(this.currentInteraction)
    }
  },
  mounted() {}
})
</script>
