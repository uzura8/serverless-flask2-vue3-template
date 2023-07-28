// Need to install luxon to use this file
import type { DateTimeFormatOptions } from 'luxon'
import type { DateTimeFormat } from '@/types/Common'
import { DateTime } from 'luxon'

export function getDateTime(utcDateStr = '', isUTC = false, locale = '') {
  let dt = utcDateStr ? DateTime.fromISO(utcDateStr) : DateTime.now()
  if (locale) dt = dt.setLocale(locale)
  dt = isUTC ? dt.toUTC() : dt
  return dt
}

export function formatIsoDate(utcDateStr = '', format = '', isUTC = false, locale = '') {
  if (!format) format = 'yyyy/MM/dd HH:mm:ss'
  const dt = getDateTime(utcDateStr, isUTC, locale)
  return dt.toFormat(format)
}

export function formatIsoDateToLocaleStr(
  utcDateStr = '',
  formatForLocale: DateTimeFormat = 'DATE_MED',
  isUTC = false,
  locale = ''
) {
  if (!formatForLocale) formatForLocale = 'DATE_MED'
  const format = getFormatForLocale(formatForLocale)
  const dt = getDateTime(utcDateStr, isUTC, locale)
  return dt.toLocaleString(format)
}

export function getFormatForLocale(format: DateTimeFormat = 'DATE_MED'): DateTimeFormatOptions {
  return DateTime[format] || DateTime.DATE_MED
}

export function formatToLocaleStrFromDatetime(
  dt: DateTime,
  formatForLocale: DateTimeFormat = 'DATE_MED'
) {
  if (!formatForLocale) formatForLocale = 'DATE_MED'
  const format = getFormatForLocale(formatForLocale)
  return dt.toLocaleString(format)
}
