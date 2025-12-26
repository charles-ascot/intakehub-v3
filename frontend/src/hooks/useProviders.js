import { useState } from 'react'

export const useProviders = () => {
  const [state, setState] = useState(null)
  return { state, setState }
}
