export type Task = {
  id: string
  title: string
  description: string
  useInputImageInChat: boolean
  useAIImageInChat: boolean
  buildSubmissionObject: (
    workspaceText: SubmissionData,
    interactionText: SubmissionData
  ) => SubmissionData
}

export type SubmissionData = {
  text: string
  image: string
  data: any
}

export type TaskInteraction = {
  task: Task
  objective: string
  interactionData: SubmissionData
  isLoading: boolean
  history: Array<DisplayMessage>
}

export type DisplayMessage = {
  text: string
  image: string
  role: string
  error: string
}
