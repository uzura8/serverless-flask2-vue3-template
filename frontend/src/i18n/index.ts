import type { I18nOptions } from 'vue-i18n'
import { createI18n } from 'vue-i18n'
import trsEn from './translations/en.json'
import trsJa from './translations/ja.json'

const locale = window.navigator.language

const messages = {
  en: trsEn,
  ja: trsJa
}

const i18nOptions: I18nOptions = {
  legacy: false,
  locale: locale,
  fallbackLocale: 'en',
  messages
}
const i18n = createI18n(i18nOptions)

export default i18n
