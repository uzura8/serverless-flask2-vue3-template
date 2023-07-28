<script lang="ts">
import { defineComponent, ref, watch, computed } from 'vue'
import { randStr } from '@/utils/str'

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
    isBlockClickable: {
      type: Boolean,
      default: false
    },
    isDispClicakbleBlockBorder: {
      type: Boolean,
      default: false
    },
    errorText: {
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
    valueTextClass: {
      type: String,
      default: ''
    },
    modelValue: Boolean
  },

  setup(props, context) {
    const inputValue = ref(props.modelValue)

    const inputId = computed(() => {
      return randStr(8)
    })

    const valueTextUnified = computed(() => {
      let vals = []
      if (props.isBlockClickable) vals.push('w-full py-4 cursor-pointer')
      if (props.valueTextClass) vals.push(props.valueTextClass)
      return vals.join(' ')
    })

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
      inputId,
      valueTextUnified
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

    <div
      class="flex items-center"
      :class="{
        'pl-4 border border-gray-200 rounded dark:border-gray-700': isDispClicakbleBlockBorder,
        'mb-4 mt-4': !isBlockClickable
      }"
    >
      <input
        v-model="inputValue"
        :id="inputId"
        type="checkbox"
        class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
      />
      <label
        :for="inputId"
        class="ml-2 font-medium text-gray-900 dark:text-gray-300"
        :class="valueTextUnified"
      >
        {{ valueText }}
      </label>
    </div>
    <p
      v-if="errorText"
      class="mt-2 text-sm text-red-600 dark:text-red-500"
    >
      {{ errorText }}
    </p>
  </div>
</template>
