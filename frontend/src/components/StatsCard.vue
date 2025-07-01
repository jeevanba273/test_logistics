<template>
  <div class="card">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <component :is="icon" class="w-8 h-8" :class="iconColor" />
      </div>
      <div class="ml-5 w-0 flex-1">
        <dl>
          <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
          <dd class="text-lg font-medium text-gray-900">{{ value }}</dd>
        </dl>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon: any
  iconColor?: string
}

withDefaults(defineProps<Props>(), {
  iconColor: 'text-primary-600'
})
</script>