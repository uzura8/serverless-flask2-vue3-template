<script lang="ts">
import type { AxiosError } from 'axios'
import type { FormSelectFieldOptionObj } from '@/types/Common'
import type { RepositoryFormVals, RepositoryUpdateFormVals } from '@/types/Repository'
import { defineComponent, ref, computed, watch, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import { useGlobalLoaderStore } from '@/stores/globalLoader.js'
import { checkUrl } from '@/utils/str'
import { RepositoryApi } from '@/apis'
import config from '@/configs/config.json'
import FormInputField from '@/components/molecules/FormInputField.vue'
import FormSelectField from '@/components/molecules/FormSelectField.vue'
import FormCheckBoxToggleField from '@/components/molecules/FormCheckBoxToggleField.vue'
import KeyValueList from '@/components/atoms/KeyValueList.vue'

interface FieldErrors {
  repoUrl: string
  serviceDomain: string
  serviceSegment: string
  repoName: string
  serverDomain: string
  isBuildRequired: string
  buildType: string
  buildTargetDirPath: string
  nodeJSVersion: string
}

export default defineComponent({
  components: {
    FormInputField,
    FormSelectField,
    FormCheckBoxToggleField,
    KeyValueList
  },

  props: {
    repoId: {
      type: String,
      required: false,
      default: ''
    },
    serverDomain: {
      type: String,
      required: false
    }
  },

  setup(props) {
    const router = useRouter()
    const { t } = useI18n()
    const globalLoader = useGlobalLoaderStore()
    const userStore = useUserStore()
    const { idToken } = storeToRefs(userStore)

    const globalErrorMsg = ref<string>('')
    const errors = ref<FieldErrors>({
      repoUrl: '',
      serviceDomain: '',
      serviceSegment: '',
      repoName: '',
      serverDomain: '',
      isBuildRequired: '',
      buildType: '',
      buildTargetDirPath: '',
      nodeJSVersion: ''
    })
    const hasErrors = computed<boolean>(() => {
      const hoge = Object.values(errors.value).some((error) => error)
      const fuga = !!globalErrorMsg.value
      return hoge || fuga
    })

    const repoInfoInputMode = ref<'url' | 'items'>('url')
    watch(repoInfoInputMode, (val) => {
      if (val === 'items') {
        errors.value.repoUrl = ''
      } else {
        errors.value.serviceDomain = ''
        errors.value.serviceSegment = ''
        errors.value.repoName = ''
      }
    })

    const repoUrl = ref<string>('')
    const serviceDomain = ref<string>('')
    const serviceSegment = ref<string>('')
    const repoName = ref<string>('')

    const validateRepoUrl = () => {
      globalErrorMsg.value = ''
      errors.value.repoUrl = ''
      errors.value.serviceDomain = ''
      errors.value.serviceSegment = ''
      errors.value.repoName = ''
      if (repoInfoInputMode.value == 'url' && !repoUrl.value) {
        errors.value.repoUrl = t('msg.inputRequired')
        return
      }
      if (!checkUrl(repoUrl.value)) {
        errors.value.repoUrl = t('msg.inputInvalid')
        return
      }
      const items = parseRepoUrl(repoUrl.value)
      if (!items) {
        errors.value.repoUrl = t('msg.inputInvalid')
        return
      }
      serviceDomain.value = items.domain
      serviceSegment.value = items.segment
      repoName.value = items.repoName
      repoUrl.value = items.url
    }

    const repoUrlItems = computed(() => {
      const res = [
        {
          label: t('pgit.form.repository.serviceDomain'),
          value: serviceDomain.value
        },
        {
          label: t('pgit.form.repository.serviceSegment'),
          value: serviceSegment.value
        },
        {
          label: t('pgit.form.repository.repoName'),
          value: repoName.value
        }
      ]
      return res
    })

    const parseRepoUrl = (url: string) => {
      const regex = /^https:\/\/(coopnext\.backlog\.jp\/git|github\.com)\/([^\/]+)\/([^\/]+)/
      const match = url.match(regex)
      if (!match) return null
      return {
        domain: match[1],
        segment: match[2],
        repoName: match[3],
        url: `https://${match[1]}/${match[2]}/${match[3]}`
      }
    }

    const serviceDomainOptionObjs: FormSelectFieldOptionObj[] = []
    config.pgit.repository.services.map((item) => {
      serviceDomainOptionObjs.push({
        label: item.label,
        value: item.domain
      })
    })
    const serviceDomainOptionVals = serviceDomainOptionObjs.map((item) => item.value)

    const validateServiceDomain = (isPost = false) => {
      globalErrorMsg.value = ''
      errors.value.serviceDomain = ''
      if (!serviceDomain.value) {
        if (isPost) {
          errors.value.serviceDomain = t('msg.inputRequired')
        }
        return
      }
      if (serviceDomainOptionVals.includes(serviceDomain.value) === false) {
        errors.value.serviceDomain = t('msg.inputInvalid')
      }
    }
    const validateServiceSegment = (isPost = false) => {
      globalErrorMsg.value = ''
      errors.value.serviceSegment = ''
      if (!serviceSegment.value) {
        if (isPost) {
          errors.value.serviceSegment = t('msg.inputRequired')
        }
        return
      }
      if (/^[a-zA-Z0-9\-_]+$/.test(serviceSegment.value) === false) {
        errors.value.serviceSegment = t('msg.inputInvalid')
      }
    }
    const validateRepoName = (isPost = false) => {
      globalErrorMsg.value = ''
      errors.value.repoName = ''
      if (!repoName.value) {
        if (isPost) {
          errors.value.repoName = t('msg.inputRequired')
        }
        return
      }
      if (/^[a-zA-Z0-9\-_]+$/.test(repoName.value) === false) {
        errors.value.repoName = t('msg.inputInvalid')
      }
    }

    const generatedRepoUrl = computed<string>(() => {
      if (!serviceDomain.value || !serviceSegment.value || !repoName.value) {
        return ''
      }
      if (errors.value.serviceDomain || errors.value.serviceSegment || errors.value.repoName) {
        return ''
      }
      return `https://${serviceDomain.value}/${serviceSegment.value}/${repoName.value}`
    })

    watch(generatedRepoUrl, (val) => {
      if (val && !repoUrl.value) {
        repoUrl.value = val
      }
    })

    const serverDomain = ref<string>(props.serverDomain || '')
    const serverDomainOptions = ['pgit.me', 'pgit.be']
    const validateServerDomain = () => {
      globalErrorMsg.value = ''
      errors.value.serverDomain = ''
      if (!serverDomain.value) {
        errors.value.serverDomain = t('msg.inputRequired')
        return
      }
      if (serverDomainOptions.includes(serverDomain.value) === false) {
        errors.value.serverDomain = t('msg.inputInvalid')
      }
    }
    const isSetServerDomain = computed<boolean>(() => {
      return !!props.serverDomain
    })

    const isBuildRequired = ref<boolean>(false)
    const validateIsBuildRequired = () => {
      globalErrorMsg.value = ''
      errors.value.isBuildRequired = ''
    }

    const buildType = ref<string>('')
    const buildTypeOptions = ['npm', 'yarn']
    const validateBuildType = () => {
      globalErrorMsg.value = ''
      errors.value.buildType = ''
      if (!isBuildRequired.value) {
        return
      }
      if (!buildType.value) {
        errors.value.buildType = t('msg.inputRequired')
        return
      }
      if (buildTypeOptions.includes(buildType.value) === false) {
        errors.value.buildType = t('msg.inputInvalid')
      }
    }

    const buildTargetDirPath = ref<string>('src')
    const validateBuildTargetDirPath = () => {
      globalErrorMsg.value = ''
      errors.value.buildTargetDirPath = ''
      if (!isBuildRequired.value) {
        return
      }
      if (!buildTargetDirPath.value) {
        errors.value.buildTargetDirPath = t('msg.inputRequired')
      }
    }

    const nodeJSVersion = ref<string>('')
    const nodeJSVersionOptions = ['18.X', '16.X', '14.X']
    const validateNodeJSVersion = () => {
      globalErrorMsg.value = ''
      errors.value.nodeJSVersion = ''
      if (!isBuildRequired.value) {
        return
      }
      if (!nodeJSVersion.value) {
        errors.value.nodeJSVersion = t('msg.inputRequired')
      }
      if (nodeJSVersionOptions.includes(nodeJSVersion.value) === false) {
        errors.value.nodeJSVersion = t('msg.inputInvalid')
      }
    }

    const isEdit = computed<boolean>(() => {
      return props.repoId !== ''
    })

    const validateAll = () => {
      globalErrorMsg.value = ''
      if (repoInfoInputMode.value === 'url') {
        validateRepoUrl()
      }
      validateServiceDomain(true)
      validateServiceSegment(true)
      validateRepoName(true)
      validateServerDomain()
      validateIsBuildRequired()
      validateBuildType()
      validateBuildTargetDirPath()
      validateNodeJSVersion()
    }

    const saveRepository = async (): Promise<void> => {
      validateAll()
      if (hasErrors.value) return

      try {
        globalLoader.updateLoading(true)
        if (!isBuildRequired.value) {
          buildType.value = ''
          buildTargetDirPath.value = 'src'
          nodeJSVersion.value = ''
        }
        let updateVals: RepositoryUpdateFormVals = {
          isBuildRequired: isBuildRequired.value,
          buildType: buildType.value,
          buildTargetDirPath: buildTargetDirPath.value,
          nodeJSVersion: nodeJSVersion.value
        }
        if (isEdit.value && props.repoId) {
          await RepositoryApi.update(props.repoId, updateVals, idToken.value)
        } else {
          let createVals: RepositoryFormVals = {
            ...{
              serviceDomain: serviceDomain.value,
              serviceSegment: serviceSegment.value,
              repoName: repoName.value,
              serverDomain: serverDomain.value
            },
            ...updateVals
          }
          await RepositoryApi.create(createVals, idToken.value)
        }
        globalLoader.updateLoading(false)
        if (isSetServerDomain.value) {
          router.push(`/servers/${serverDomain.value}/repositories`)
        } else {
          router.push('/repositories')
        }
      } catch (error) {
        const apiError = error as AxiosError
        if (apiError.response?.status === 409) {
          globalErrorMsg.value = t('msg.alreadyRegistered')
        } else {
          console.error(error)
        }
        globalLoader.updateLoading(false)
      }
    }

    const setRepository = async () => {
      try {
        if (!props.repoId) return
        globalLoader.updateLoading(true)
        const repo = await RepositoryApi.getOne(props.repoId, idToken.value)
        serviceDomain.value = repo.serviceDomain
        serviceSegment.value = repo.serviceSegment
        repoName.value = repo.repoName
        serverDomain.value = repo.serverDomain
        isBuildRequired.value = repo.isBuildRequired
        buildType.value = repo.buildType ? repo.buildType : ''
        buildTargetDirPath.value = repo.buildTargetDirPath ? repo.buildTargetDirPath : ''
        nodeJSVersion.value = repo.nodeJSVersion ? repo.nodeJSVersion : ''
        globalLoader.updateLoading(false)
      } catch (error) {
        console.error(error)
        globalLoader.updateLoading(false)
      }
    }

    onBeforeMount(async () => {
      if (isEdit.value) {
        await setRepository()
      }
    })

    return {
      isEdit,
      saveRepository,
      globalErrorMsg,
      errors,
      hasErrors,
      repoUrl,
      validateRepoUrl,
      serviceDomain,
      validateServiceDomain,
      serviceSegment,
      validateServiceSegment,
      repoName,
      validateRepoName,
      repoUrlItems,
      generatedRepoUrl,
      serviceDomainOptionObjs,
      repoInfoInputMode,
      serverDomain,
      serverDomainOptions,
      validateServerDomain,
      isSetServerDomain,
      isBuildRequired,
      validateIsBuildRequired,
      buildType,
      buildTypeOptions,
      validateBuildType,
      buildTargetDirPath,
      validateBuildTargetDirPath,
      nodeJSVersion,
      nodeJSVersionOptions,
      validateNodeJSVersion
    }
  }
})
</script>

<template>
  <div class="grid gap-10">
    <div>
      <h3 class="text-lg font-medium dark:text-white">
        <span>{{ $t('pgit.form.repository.repoInfo') }}</span>
      </h3>
      <ul
        v-if="!isEdit"
        class="my-6 flex flex-wrap text-sm font-medium text-center text-gray-500 dark:text-gray-400"
      >
        <li class="mr-2">
          <button
            @click="repoInfoInputMode = 'url'"
            type="button"
            class="inline-block px-4 py-3 rounded-lg"
            :class="{
              'text-white bg-blue-600 active': repoInfoInputMode === 'url',
              'hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white':
                repoInfoInputMode !== 'url'
            }"
            aria-current="page"
          >
            {{ $t('pgit.form.repository.inputByUrl') }}
          </button>
        </li>
        <li class="mr-2">
          <button
            @click="repoInfoInputMode = 'items'"
            type="button"
            class="inline-block px-4 py-3 rounded-lg"
            :class="{
              'text-white bg-blue-600 active': repoInfoInputMode === 'items',
              'hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-800 dark:hover:text-white':
                repoInfoInputMode !== 'items'
            }"
          >
            {{ $t('pgit.form.repository.inputEachItems') }}
          </button>
        </li>
      </ul>

      <div v-if="!isEdit">
        <div v-if="repoInfoInputMode === 'url'">
          <FormInputField
            v-model="repoUrl"
            :errorText="errors.repoUrl"
            :label-text="$t('pgit.form.repository.repoUrl')"
            @blur="validateRepoUrl"
          />
          <div
            v-if="repoUrl && !errors['repoUrl']"
            class="mt-4 p-4 bg-gray-50 rounded"
          >
            <KeyValueList :items="repoUrlItems" />
          </div>
        </div>
        <div v-else>
          <FormSelectField
            v-model="serviceDomain"
            :errorText="errors.serviceDomain"
            :optionObjs="serviceDomainOptionObjs"
            :default-option-text="$t('msg.pleaseSelect')"
            :label-text="$t('pgit.form.repository.service')"
            @change="validateServiceDomain"
          />
          <FormInputField
            v-model="serviceSegment"
            @blur="validateServiceSegment"
            :label-text="$t('pgit.form.repository.serviceSegment')"
            :errorText="errors.serviceSegment"
            :helper-text="$t('pgit.form.repository.serviceSegmentHelpText')"
            class="mt-6"
          />
          <FormInputField
            v-model="repoName"
            :errorText="errors.repoName"
            :label-text="$t('pgit.form.repository.repoName')"
            @blur="validateRepoName"
            class="mt-6"
          />
        </div>
      </div>
      <div
        v-if="generatedRepoUrl"
        class="mt-8"
      >
        <label class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
          <span v-if="isEdit">{{ $t('pgit.form.repository.repoUrl') }}</span>
          <span v-else>{{
            $t('common.generatedOf', { label: $t('pgit.form.repository.repoUrl') })
          }}</span>
        </label>
        <div class="p-4 bg-gray-50 rounded italic text-gray-700">
          {{ generatedRepoUrl }}
        </div>
      </div>
    </div>
    <div>
      <h3 class="text-lg font-medium dark:text-white">
        <span>{{ $t('pgit.term.server') }}</span>
      </h3>
      <span
        v-if="isSetServerDomain || isEdit"
        class="mt-4"
      >
        {{ serverDomain }}
      </span>
      <FormSelectField
        v-else
        v-model="serverDomain"
        :errorText="errors.serverDomain"
        :options="serverDomainOptions"
        :default-option-text="$t('msg.pleaseSelect')"
        :label-text="$t('pgit.form.repository.serverDomain')"
        @change="validateServerDomain"
        class="mt-4"
      />
    </div>
    <div>
      <h3 class="text-lg font-medium dark:text-white">
        <span>{{ $t('pgit.form.repository.buildInfo') }}</span>
      </h3>
      <FormCheckBoxToggleField
        v-model="isBuildRequired"
        :errorText="errors.isBuildRequired"
        :value-text="$t('pgit.form.repository.isBuildRequired')"
        @blur="validateIsBuildRequired"
        class="mt-4"
      />
      <div v-if="isBuildRequired">
        <FormSelectField
          v-model="nodeJSVersion"
          :errorText="errors.nodeJSVersion"
          :options="nodeJSVersionOptions"
          :default-option-text="$t('msg.pleaseSelect')"
          :label-text="$t('pgit.form.repository.nodeJSVersion')"
          @change="validateNodeJSVersion"
          class="mt-4"
        />
        <FormSelectField
          v-model="buildType"
          :errorText="errors.buildType"
          :options="buildTypeOptions"
          :label-text="$t('pgit.form.repository.buildType')"
          @change="validateBuildType"
          class="mt-6"
        />
        <FormInputField
          v-model="buildTargetDirPath"
          :errorText="errors.buildTargetDirPath"
          :label-text="$t('pgit.form.repository.buildTargetDirPath')"
          @blur="validateBuildTargetDirPath"
          class="mt-6"
        />
        <div
          v-if="buildType && !errors['buildType']"
          class="mt-8"
        >
          <span class="text-sm text-gray-900 dark:text-white">{{
            $t('pgit.form.repository.buildHelpText')
          }}</span>
          <div class="mt-2 p-4 text-gray-600 bg-gray-50 rounded italic">
            <div v-if="buildType === 'npm'">
              npm install
              <span class="text-gray-400"> // package.json に変更があった場合のみ実施</span><br />
              npm run build
              <span class="text-gray-400">
                // ビルド対象ディレクトリに変更があった場合のみ実施</span
              >
            </div>
            <div v-if="buildType === 'yarn'">
              yarn install
              <span class="text-gray-400"> // package.json に変更があった場合のみ実施</span><br />
              yarn build
              <span class="text-gray-400">
                // ビルド対象ディレクトリに変更があった場合のみ実施
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div
        v-if="globalErrorMsg || hasErrors"
        class="text-red-600 dark:text-red-500"
      >
        <p v-if="globalErrorMsg">
          {{ globalErrorMsg }}
        </p>
        <p v-else-if="hasErrors">
          {{ $t('msg.errorsExist') }}
        </p>
      </div>
      <div class="text-center">
        <button
          @click="saveRepository"
          type="button"
          :disabled="hasErrors"
          class="w-full max-w-md mt-8 font-medium text-center focus:ring-4 focus:outline-none rounded-lg focus:ring-blue-300"
          :class="{
            'px-3 py-2 text-white bg-blue-700 hover:bg-blue-800 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800':
              !isEdit,
            'text-blue-700 hover:text-white border border-blue-700 hover:bg-blue-800 text-sm px-5 py-2.5 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-500 dark:focus:ring-blue-800':
              isEdit
          }"
          v-text="isEdit ? $t('common.update') : $t('common.add')"
        ></button>
      </div>
    </div>
  </div>
</template>
