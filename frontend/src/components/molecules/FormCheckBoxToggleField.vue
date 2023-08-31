<script lang="ts">
import { defineComponent, ref, watch } from 'vue'

export default defineComponent({
  props: {
    labelText: {
      type: String,
      required: false,
      default: ''
    },
    errorText: {
      type: String,
      default: ''
    },
    helperText: {
      type: String,
      default: ''
    },
    isRequired: {
      type: Boolean,
      default: false
    },
    valueText: {
      type: String,
      default: ''
    },
    modelValue: Boolean
  },

  setup(props, context) {
    const inputValue = ref(props.modelValue)

    const toggle = () => {
      inputValue.value = !inputValue.value
      //context.emit('update:modelValue', inputValue.value)
    }

    watch(
      () => props.modelValue,
      (value) => {
        inputValue.value = value
      }
    )

    watch(inputValue, (value) => {
      context.emit('update:modelValue', value)
    })

    return {
      inputValue,
      toggle
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

    <label class="relative inline-flex items-center cursor-pointer">
      <input
        type="checkbox"
        v-model="inputValue"
        class="sr-only peer"
        @input="toggle"
      />
      <div
        class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
      ></div>
      <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">
        {{ valueText }}
      </span>
    </label>
    <p
      v-if="errorText"
      class="mt-2 text-sm text-red-600 dark:text-red-500"
    >
      {{ errorText }}
    </p>
    <p
      v-if="helperText"
      class="mt-1 text-xs font-medium text-gray-500"
    >
      {{ helperText }}
    </p>
  </div>
</template>
