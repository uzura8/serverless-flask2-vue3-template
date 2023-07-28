export function substr(text: string, len: number, truncation = ''): string {
  const textArray = text.split('')
  let count = 0
  let str = ''
  for (let i = 0, m = textArray.length; i < m; i++) {
    const n = escape(textArray[i])
    if (n.length < 4) {
      count++
    } else {
      count += 2
    }
    if (count > len) {
      return str + truncation
    }
    str += text.charAt(i)
  }
  return text
}

export function checkEmail(text: string): boolean {
  // eslint-disable-next-line no-useless-escape
  const regexp =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return regexp.test(text)
}

export function nl2br(str: string): string {
  if (str == null) return ''
  str = str.replace(/\r\n/g, '<br />')
  str = str.replace(/(\n|\r)/g, '<br />')
  return str
}

export function link2url(text: string, isTargetBlank = true, classStr = ''): string {
  const regexp = /(https?|ftp|file):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]/g
  return text.replace(regexp, (url) => {
    const target = isTargetBlank ? ' target="_blank"' : ''
    return `<a href="${url}" class="${classStr}"${target}>${url}</a>`
  })
}

export function getOrdinalNumber(n: number): string {
  const s = ['th', 'st', 'nd', 'rd'],
    v = n % 100
  return n + (s[(v - 20) % 10] || s[v] || s[0])
}

export function getLocaleOrdinalNumber(num: number, locale = 'en'): string {
  if (locale === 'ja') return `第${num}`
  return getOrdinalNumber(num)
}

export function randStr(length: number): string {
  let result = ''
  const characters = 'abcdefghijklmnopqrstuvwxyz'
  const charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

export function capitalize(string: string): string {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

export function numFormat(num: number | string): string {
  if (typeof num === 'string') num = parseFloat(num)
  if (isNaN(num)) return ''
  return num.toLocaleString()
}
