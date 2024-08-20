import type { Task, SubmissionData } from '@/stores/types'

function buildSubmissionObject(workspaceData: SubmissionData, interactionData: SubmissionData) {
  // this is pretty simplistic here.
  return { text: interactionData.text, image: workspaceData.image, data: {} }
}

export const tangram_task = {
  id: 'tangram',
  title: 'Tangram design Task',
  description: `The objective of this task is to use a tangram game to collaboratively fullfil a task together with an AI. 
                    The player and the AI take turns in placing (or moving) pieces of a tangram game. 
                    Please define what task you and the AI will be working on.`,
  buildSubmissionObject: buildSubmissionObject,
  useInputImageInChat: false,
  useAIImageInChat: false
} as Task
