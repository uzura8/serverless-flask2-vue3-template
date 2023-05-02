interface Site {
  name: string
  footerRight: string
}

interface Common {
  loadingMaxDuration: number
}

interface Api {
  origin: string
  basePath: string
}

interface Post {
  serviceId: string
}

export interface Config {
  site: Site
  common: Common
  api: Api
  post: Post
}

declare module '@/configs/config.json' {
  const config: Config

  export default config
}
