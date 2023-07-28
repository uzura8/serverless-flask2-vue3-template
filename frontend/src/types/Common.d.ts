//export type NumericString = string & { __numericStringBrand: never }

export interface File {
  fileId: string
  mimeType: string
  caption: string
}

export interface ApiParams {
  token?: string
  [key: string]: string | number | boolean
}

export type DateTimeFormat =
  | 'DATE_SHORT'
  | 'DATE_MED'
  | 'DATE_MED_WITH_WEEKDAY'
  | 'DATE_FULL'
  | 'DATE_HUGE'
  | 'TIME_SIMPLE'
  | 'TIME_WITH_SECONDS'
  | 'TIME_WITH_SHORT_OFFSET'
  | 'TIME_WITH_LONG_OFFSET'
  | 'TIME_24_SIMPLE'
  | 'TIME_24_WITH_SECONDS'
  | 'TIME_24_WITH_SHORT_OFFSET'
  | 'TIME_24_WITH_LONG_OFFSET'
  | 'DATETIME_SHORT'
  | 'DATETIME_MED'
  | 'DATETIME_FULL'
  | 'DATETIME_HUGE'
  | 'DATETIME_SHORT_WITH_SECONDS'
  | 'DATETIME_MED_WITH_SECONDS'
  | 'DATETIME_FULL_WITH_SECONDS'
  | 'DATETIME_HUGE_WITH_SECONDS'
