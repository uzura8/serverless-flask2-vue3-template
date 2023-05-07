export default {
  substr(text: string, len: number, truncation = ''): string {
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
  },

  trimSpaces(str: string): string {
    return str.replace(/^[ \t\n\r\u3000]+|[ \t\n\r\u3000]+$/g, '')
  },

  checkEmail(text: string): boolean {
    const regexp =
      /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return regexp.test(text)
  }
}
