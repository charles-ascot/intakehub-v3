import create from 'zustand'

export const healthStore = create((set) => ({
  // TODO: Add store state and actions
  state: null,
  setState: (newState) => set({ state: newState })
}))
