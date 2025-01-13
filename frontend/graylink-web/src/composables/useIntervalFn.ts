import { ref, onUnmounted } from 'vue'

interface IntervalFnReturn {
  resume: () => void
  pause: () => void
  isActive: () => boolean
}

export function useIntervalFn(
  fn: () => void | Promise<void>,
  interval: number
): IntervalFnReturn {
  const timer = ref<number | null>(null)

  const stop = () => {
    if (timer.value) {
      clearInterval(timer.value)
      timer.value = null
    }
  }

  const start = () => {
    stop()
    timer.value = setInterval(fn, interval) as unknown as number
  }

  const isActive = () => timer.value !== null

  onUnmounted(() => {
    stop()
  })

  return {
    resume: start,
    pause: stop,
    isActive
  }
} 