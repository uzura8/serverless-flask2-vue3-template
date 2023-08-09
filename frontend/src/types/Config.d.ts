import type { GameType, DurationUnit, MatchResultType } from './Game'

interface Site {
  name: string
  footerRight: string
}

interface Common {
  loadingMaxDuration: number
}

interface AuthHeaderItem {
  name: string
  tokenPrefix: string
}

interface AuthHeader {
  user: AuthHeaderItem
  admin: AuthHeaderItem
}

interface Api {
  origin: string
  basePath: string
  authHeader: AuthHeader
}

interface RepositoryService {
  label: string
  domain: string
}

interface Repository {
  services: RepositoryService[]
}

interface Pgit {
  repository: Repository
}

interface Post {
  serviceId: string
}

export interface Config {
  site: Site
  common: Common
  api: Api
  pgit: Pgit
  post: Post
}

declare module '@/configs/config.json' {
  const config: Config

  export default config
}
