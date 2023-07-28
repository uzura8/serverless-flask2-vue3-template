import VueSanitize from 'vue-3-sanitize'

declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $sanitize: typeof VueSanitize
  }
}
