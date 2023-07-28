import { useI18n } from 'vue-i18n'
import { getLocaleOrdinalNumber } from '@/utils/str'

export const useLocaleText = () => {
  const { t, locale } = useI18n()

  const localeGameNumberLabel = (gameNumber: number): string => {
    return t('sl.term.gameNumber', {
      num: getLocaleOrdinalNumber(gameNumber, locale.value)
    })
  }

  return {
    localeGameNumberLabel
  }
}
