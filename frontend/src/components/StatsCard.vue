<template>
  <div class="card animate-bounce-in">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <div :class="iconBgClass" class="w-12 h-12 rounded-lg flex items-center justify-center">
          <component :is="icon" :class="iconClass" class="w-6 h-6" />
        </div>
      </div>
      <div class="ml-4 flex-1">
        <p class="text-sm font-medium text-gray-500 uppercase tracking-wide">{{ title }}</p>
        <p class="text-2xl font-bold text-gray-900">{{ value }}</p>
        <p v-if="subtitle" class="text-sm text-gray-600 mt-1">{{ subtitle }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  value: string | number
  subtitle?: string
  icon: any
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple'
}

const props = withDefaults(defineProps<Props>(), {
  color: 'blue'
})

const iconBgClass = computed(() => {
  const classes = {
    blue: 'bg-blue-100',
    green: 'bg-green-100',
    yellow: 'bg-yellow-100',
    red: 'bg-red-100',
    purple: 'bg-purple-100'
  }
  return classes[props.color]
})

const iconClass = computed(() => {
  const classes = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    yellow: 'text-yellow-600',
    red: 'text-red-600',
    purple: 'text-purple-600'
  }
  return classes[props.color]
})
</script>