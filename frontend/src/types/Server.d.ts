type IsExecuting = '0' | '1'
export type ServerDeployStatusForRequest = 'start' | 'finish'

export interface Server {
  domain: string
  deployStatus: string
  isExecuting: IsExecuting
  createdAt: string
  updatedAt: string
}

export interface ServersApiResult {
  items: Server[]
  pagerKey?: PagerKey
}
