<script lang="ts">
import type { FormSelectFieldOptionObj } from '@/types/Common'
import type { PropType } from 'vue'
import { defineComponent, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  props: {
    labelText: {
      type: String,
      required: false,
      default: ''
    },
    options: {
      type: Array as PropType<string[]>,
      required: false
    },
    optionObjs: {
      type: Array as PropType<FormSelectFieldOptionObj[]>,
      required: false
    },
    defaultOptionText: {
      type: String,
      required: false
    },
    errorText: {
      type: String,
      required: false,
      default: ''
    },
    optionsLabelTransKey: {
      type: String,
      required: false
    },
    isWidthFull: {
      type: Boolean,
      required: false,
      default: true
    },
    isRequired: {
      type: Boolean,
      required: false,
      default: false
    },
    modelValue: {
      type: String,
      required: false,
      default: ''
    }
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
      if (!props.optionsLabelTransKey) return key
      return t(`${props.optionsLabelTransKey}.${key}`)
    }

    return {
      selectedValue,
      optionText
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
        v-if="optionObjs"
        v-for="optionObj in optionObjs"
        :value="optionObj.value"
        :selected="optionObj.value === selectedValue"
        v-text="optionObj.label"
      ></option>
      <option
        v-else
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
