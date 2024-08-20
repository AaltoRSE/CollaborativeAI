# CollaborativeAI Frontend

This frontend consists of a vue framework using primevue for components and primeflex for layouting.
It provides a general framework and task specific parts that can easily be adapted for a specific task.

General Structure:

src/components - General components
src/tasks - Task Components and data, one folder for each task. Folder needs to contain a "Component.vue" and a "types.ts" file, which will be used for the respective task.
src/stores - All stores
src/views - all SPA views (mainly Welcome and Tasks)

## Component modifications

The idea is to have a general chat on the right hand side (handled in src/components/ConversationDisplay.vue with inputs in `src/tasks/Interaction.vue`) and a task specific component (in `src/tasks/Workspace.vue`) on the right.
Interaction.vue emits a `submit` event with the user input. This activates the submission process. During submission the `getSubmissionData` function from the Workspace component is queried and needs to provide additional data necessary for the submission (if any).
Overall these are the two components you can easily modify to provide images from the workspace, or other data from there.   

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
