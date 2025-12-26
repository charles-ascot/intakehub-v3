import { useState } from 'react'

export const useHealth = () => {
  const [state, setState] = useState(null)
  return { state, setState }
}
