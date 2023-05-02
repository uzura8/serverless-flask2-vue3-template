import { str } from '@/utils'

export default {
  substr(text: string, num: number) {
    return str.substr(text, num, '...')
  },
}
