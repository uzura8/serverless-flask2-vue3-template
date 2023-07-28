export function hasKey(
  obj: Record<string, unknown>,
  prop: string,
  checkEmpty: boolean = false
): boolean {
  if (typeof obj !== 'object') return false
  if (Array.isArray(obj)) return false
  if (!Object.prototype.hasOwnProperty.call(obj, prop)) return false
  if (!(prop in obj)) return false
  if (obj[prop] == null) return false
  if (!checkEmpty) return true
  return Boolean(obj[prop])
}

export function isEmpty(data: unknown): boolean {
  if (
    data === null ||
    data === undefined ||
    data === false ||
    data === '' ||
    data === '0' ||
    data === 0
  ) {
    return true
  }

  if (typeof data === 'object') {
    if (Array.isArray(data)) return data.length === 0
    if (Object.keys(data as Record<string, unknown>).length > 0) return false
    if (
      typeof Object.getOwnPropertySymbols !== 'undefined' &&
      Object.getOwnPropertySymbols(data).length > 0
    )
      return false

    const valueOfData = (data as { valueOf(): unknown }).valueOf()
    if (typeof valueOfData === 'string' || Array.isArray(valueOfData)) {
      return valueOfData.length === 0
    } else if (typeof valueOfData !== 'object') {
      return isEmpty(valueOfData)
    }
  }
  return false
}
