export default {
  substr(text: string, len: number, truncation='') :string {
    const textArray = text.split('')
    let count = 0
    let str = ''
    for (let i = 0, m = textArray.length; i < m; i++) {
      const n = escape(textArray[i])
      if (n.length < 4) {
        count++
      } else {
        count += 2;
      }
      if (count > len) {
        return str + truncation
      }
      str += text.charAt(i)
    }
    return text
  }
}
