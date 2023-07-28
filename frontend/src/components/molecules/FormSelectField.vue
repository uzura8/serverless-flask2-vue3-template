<script lang="ts">
import type { PropType } from 'vue'
import { defineComponent, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { capitalize } from '@/utils/str'

export default defineComponent({
  props: {
    labelText: {
      type: String,
      required: false,
      default: ''
    },
    options: {
      type: Array as PropType<string[]>,
      required: true
    },
    defaultOptionText: {
      type: String
    },
    errorText: {
      type: String,
      default: ''
    },
    optionsLabelTransKey: {
      type: String,
      required: false
    },
    isWidthFull: {
      type: Boolean,
      default: true
    },
    isRequired: {
      type: Boolean,
      default: false
    },
    isInline: {
      type: Boolean,
      default: false
    },
    modelValue: String
  },

  setup(props, context) {
    const { t } = useI18n()

    const selectedValue = ref(props.modelValue)

    watch(
      () => props.modelValue,
      (value) => {
        selectedValue.value = value
      }
    )

    watch(selectedValue, (value, oldValue) => {
      context.emit('update:modelValue', value)
      context.emit('change', value, oldValue)
    })

    const optionText = (key: string) => {
      if (props.optionsLabelTransKey) {
        return t(`${props.optionsLabelTransKey}.${key}`)
      }
      return capitalize(key)
    }

    return {
      selectedValue,
      optionText
    }
  }
})
</script>

<template>
  <div :class="{ 'flex items-center space-x-4': isInline }">
    <label
      v-if="labelText"
      class="mb-2 text-sm font-medium text-gray-900 dark:text-white"
      :class="{
        'text-red-700': errorText,
        'dark:text-red-500': errorText,
        block: !isInline
      }"
    >
      <span>{{ labelText }}</span>
      <span
        v-if="isRequired"
        class="text-red-700 text-xs ml-2"
      >
        {{ $t('form.required') }}
      </span>
    </label>

    <select
      v-model="selectedValue"
      class="bg-gray-50 border text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      :class="{
        'w-full': isWidthFull,
        'border-gray-300': !errorText,
        'bg-red-50 border-red-500 text-red-900 placeholder-red-700 focus:ring-red-500 focus:border-red-500 dark:text-red-500 dark:placeholder-red-500 dark:border-red-500':
          errorText
      }"
    >
      <option
        v-if="defaultOptionText"
        value=""
      >
        {{ defaultOptionText }}
      </option>
      <option
        v-for="optionValue in options"
        :key="optionValue"
        :value="optionValue"
        :selected="optionValue === selectedValue"
        v-text="optionText(optionValue)"
      ></option>
    </select>
    <p
      v-if="errorText"
      class="mt-2 text-sm text-red-600 dark:text-red-500"
    >
      {{ errorText }}
    </p>
  </div>
</template>
