interface LastCommitInfo {
  hash: string
  authorName: string
  message: string
  date: string
}

export interface Branch {
  repoId: string
  branchId: string
  branchName: string
  repoCode: string
  serverDomain: string
  serviceDomain: string
  serviceSegment: string
  repoName: string
  lastCommitInfo: LastCommitInfo
  createdAt: string
  updatedAt?: string
}

export interface BranchesApiResult {
  items: Branch[]
  pagerKey?: PagerKey
}
