export interface RepositoryFormVals {
  serviceDomain: string
  serviceSegment: string
  repoName: string
  serverDomain: string
  isBuildRequired: boolean
  buildType?: string
  buildTargetDirPath?: string
  nodeJSVersion?: string
}

export interface Repository extends RepositoryFormVals {
  repoId: string
  createdAt: string
  updatedAt?: string
}

export interface RepositoryApiResult {
  items: Repository[]
  pagerKey?: PagerKey
}
