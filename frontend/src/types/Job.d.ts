export interface Job {
  jobId: string
  serverDomain: string
  serviceDomain: string
  serviceSegment: string
  repoName: string
  repoId: string
  repoCode: string
  branchName: string
  deployStatus: string
  deployType: string
  isBuildRequired: boolean
  buildType?: string
  buildTargetDirPath?: string
  nodeJSVersion?: string
  createdAt: string
  updatedAt?: string
}

export interface JobsApiResult {
  items: Job[]
  pagerKey?: PagerKey
}
