import moment from 'moment'
import 'moment/dist/locale/ja'
//import i18n from '@/i18n'

//moment.locale(i18n.global.locale)
const locale = window.navigator.language
moment.locale(locale)

export default moment
