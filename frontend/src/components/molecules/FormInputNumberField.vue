<script lang="ts">
import type { PropType } from 'vue'
import { defineComponent, ref, watch, computed } from 'vue'

export default defineComponent({
  props: {
    inputClass: {
      type: String,
      default: ''
    },
    labelText: {
      type: String,
      required: false,
      default: ''
    },
    errorText: {
      type: String,
      default: ''
    },
    isRequired: {
      type: Boolean,
      default: false
    },
    unitText: {
      type: String,
      default: ''
    },
    modelValue: {
      type: Number as PropType<number | '' | null>,
      default: 0
    }
  },

  setup(props, context) {
    const inputValue = ref(props.modelValue)
    watch(
      () => props.modelValue,
      (value) => {
        inputValue.value = value
      }
    )
    watch(inputValue, (value) => {
      context.emit('update:modelValue', value)
    })
    const increment = () => {
      const value = inputValue.value ? inputValue.value : 0
      context.emit('update:modelValue', value + 1)
    }
    const decrement = () => {
      const value = inputValue.value ? inputValue.value : 0
      let emitValue = value - 1
      if (emitValue < 0) emitValue = 0
      context.emit('update:modelValue', emitValue)
    }

    const inputClassStr = computed(() => {
      let classes = props.inputClass ? props.inputClass.split(' ') : []
      if (props.errorText) {
        classes = classes.concat([
          'bg-red-50',
          'border-red-500',
          'text-red-900',
          'placeholder-red-700',
          'focus:ring-red-500',
          'focus:border-red-500',
          'dark:text-red-500',
          'dark:placeholder-red-500',
          'dark:border-red-500'
        ])
      } else {
        classes = classes.concat(['border-gray-300'])
      }
      return classes.join(' ')
    })

    return {
      inputValue,
      increment,
      decrement,
      inputClassStr
    }
  }
})
</script>

<template>
  <div>
    <label
      v-if="labelText"
      class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
      :class="{ 'text-red-700': errorText, 'dark:text-red-500': errorText }"
    >
      <span>{{ labelText }}</span>
      <span
        v-if="isRequired"
        class="text-red-700 text-xs ml-2"
      >
        {{ $t('form.required') }}
      </span>
    </label>
    <div class="flex items-center">
      <button
        @click="decrement"
        type="button"
        class="mr-2 bg-gray-50 border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <FontAwesomeIcon
          icon="minus"
          class="w-3 h-3"
        />
      </button>
      <input
        v-model="inputValue"
        @blur="$emit('blur', inputValue)"
        type="number"
        class="bg-gray-50 border text-gray-900 text-lg rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        :class="inputClassStr"
      />
      <button
        @click="increment"
        type="button"
        class="ml-2 bg-gray-50 border-gray-300 text-gray-900 text-sm rounded-lg p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      >
        <FontAwesomeIcon
          icon="plus"
          class="w-3 h-3"
        />
      </button>
      <span
        v-if="unitText"
        class="ml-3"
        >{{ unitText }}</span
      >
    </div>
    <p
      v-if="errorText"
      class="mt-2 text-sm text-red-600 dark:text-red-500"
    >
      {{ errorText }}
    </p>
  </div>
</template>
