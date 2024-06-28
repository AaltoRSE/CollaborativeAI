import { defineStore } from 'pinia'
import axios from 'axios'
import type { Task, TaskInteraction, SubmissionData, DisplayMessage } from './types'

const taskField = 'CollaborativeAI:Task'
const interactionField = 'CollaborativeAI:Interaction'
import { tangram_task } from '@/tasks/currentTask'
export const useTaskStore = defineStore({
  id: 'tasks',
  state: () => ({
    task: tangram_task as Task,
    currentInteraction: (sessionStorage.getItem(interactionField)
      ? JSON.parse(sessionStorage.getItem(interactionField) as string)
      : {}) as TaskInteraction, // Maybe we can define this type later, but it is likely to be quite specific per task...
    lastInteraction: {} as SubmissionData
  }),
  actions: {
    /**
     * Select a task from the list of tasks
     * @param task
     */
    startTask() {
      sessionStorage.setItem(taskField, JSON.stringify(this.task))
      this.currentInteraction = {
        task: this.task,
        objective: '',
        interactionData: {} as SubmissionData,
        isLoading: false,
        history: []
      }
      this.storeInteraction()
    },
    /**
     * Set the objective of the current interaction
     */
    setObjective(objective: string) {
      // When we set the objective, we also start the task
      this.startTask()
      this.currentInteraction.objective = objective
      this.storeInteraction()
    },
    /**
     * Stores the current Interaction in the store
     */
    storeInteraction() {
      sessionStorage.setItem(interactionField, JSON.stringify(this.currentInteraction))
    },
    /**
     * Submit user input to the backend.
     * This triggers the currentInteraction to go into a isLoading stage
     * The data submitted is task specific and
     * @param data
     */
    submitUserInput(data: SubmissionData) {
      this.currentInteraction.isLoading = true
      console.log('Pushing to history')
      console.log(data)
      this.currentInteraction.history.push({
        text: data.text,
        image: this.task.useInputImageInChat ? data.image : '',
        role: 'user',
        error: ''
      })
      this.storeInteraction()

      axios
        .post(`/api/v1/task/process`, {
          text: data.text,
          inputData: data.data,
          image: data.image,
          objective: this.currentInteraction.objective
        })
        .then((response) => {
          // Handle response
          console.log(response)
          const responseData = response.data
          const submissiondata = { tangram: responseData.text }
          this.lastInteraction = {
            text: responseData.text,
            image: responseData.image,
            data: submissiondata
          } as SubmissionData
          this.currentInteraction.history.push({
            text: responseData.text,
            image: this.task.useAIImageInChat ? responseData.image : '',
            role: 'AI',
            error: ''
          })
          sessionStorage.setItem(interactionField, JSON.stringify(this.currentInteraction))
          this.currentInteraction.isLoading = false
        })
        .catch((error) => {
          this.currentInteraction.history.push({
            role: 'AI',
            image: '',
            text: 'AI submission errored',
            error: error
          })
          this.currentInteraction.isLoading = false
        })
    },
    /**
     * Finish the task, resetting history and everything.
     */
    finishTask(rating: any) {
      const ratingjson = { metrics: rating }
      axios
        .post(`/api/v1/task/finish`, ratingjson)
        .then((response) => {
          // successfully submitted data.
          this.currentInteraction = {} as TaskInteraction
          sessionStorage.removeItem(taskField)
          sessionStorage.removeItem(interactionField)
          this.lastInteraction = {} as SubmissionData
        })
        .catch(() => {
          this.currentInteraction = {} as TaskInteraction
          sessionStorage.removeItem(taskField)
          sessionStorage.removeItem(interactionField)
          this.lastInteraction = {} as SubmissionData
        })
    }
  }
})
