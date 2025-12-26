import { useState } from 'react'

export const useAuth = () => {
  const [state, setState] = useState(null)
  return { state, setState }
}
