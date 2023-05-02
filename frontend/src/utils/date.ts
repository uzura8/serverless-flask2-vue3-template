import moment from '@/moment'

export default {
  formatDate(date: string, format = 'LLL'): string {
    return moment(date).format(format)
  }
}
