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

export interface RepositoryUpdateFormVals {
  isBuildRequired: boolean
  buildType?: string
  buildTargetDirPath?: string
  nodeJSVersion?: string
}

export interface Repository extends RepositoryFormVals {
  repoId: string
  deployStatus: string
  createdAt: string
  updatedAt?: string
}

export interface RepositoriesApiResult {
  items: Repository[]
  pagerKey?: PagerKey
}
