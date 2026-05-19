import { onBeforeUnmount, ref, watch, type Ref } from 'vue'

export function useAnimatedNumber(source: Ref<number>, duration = 900) {
  const display = ref(source.value)
  let frame = 0

  const animate = (from: number, to: number) => {
    cancelAnimationFrame(frame)
    const start = performance.now()
    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 4)
      display.value = from + (to - from) * eased
      if (progress < 1) {
        frame = requestAnimationFrame(tick)
      }
    }
    frame = requestAnimationFrame(tick)
  }

  watch(source, (next, previous) => animate(previous, next), { immediate: false })

  onBeforeUnmount(() => cancelAnimationFrame(frame))

  return display
}
