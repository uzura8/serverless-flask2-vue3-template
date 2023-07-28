import type { DateTimeFormat } from '@/types/Common'
import { useI18n } from 'vue-i18n'
import { formatIsoDate, formatIsoDateToLocaleStr } from '@/utils/date'

export const useDate = () => {
  const { locale } = useI18n()

  const formatDate = (utcDateStr = '', format = ''): string => {
    return formatIsoDate(utcDateStr, format, false, locale.value)
  }

  const localeDate = (utcDateStr = '', format: DateTimeFormat = 'DATE_MED'): string => {
    return formatIsoDateToLocaleStr(utcDateStr, format, false, locale.value)
  }

  return {
    formatDate,
    localeDate
  }
}
