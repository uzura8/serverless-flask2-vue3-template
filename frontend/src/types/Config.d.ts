import type { GameType, DurationUnit, MatchResultType } from './Game'

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

interface Temperature {
  defaultUnit: string
  defaultValue: number
}

interface EventConfig {
  temperature: Temperature
}

interface GameConfig {
  defaultGameType: GameType
  defaultDefaultResultType: MatchResultType
  defaultDurationUnit: DurationUnit
  defaultDurationValue: number
}

interface SurvaLogConfig {
  event: EventConfig
  game: GameConfig
}

export interface Config {
  site: Site
  common: Common
  api: Api
  post: Post
  sl: SurvaLogConfig
  game: Game
}

declare module '@/configs/config.json' {
  const config: Config

  export default config
}
