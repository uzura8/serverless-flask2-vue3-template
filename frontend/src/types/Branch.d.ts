import type { Repository } from './Repository'

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

interface BranchesApiResultMeta {
  repository: Repository
}

export interface BranchesApiResult {
  items: Branch[]
  pagerKey?: PagerKey
  meta?: BranchesApiResultMeta
}
