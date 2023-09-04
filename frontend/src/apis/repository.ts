import type { AxiosResponse, AxiosError } from 'axios'
import type {
  RepositoriesApiResult,
  Repository,
  RepositoryFormVals,
  RepositoryUpdateFormVals
} from '@/types/Repository'
import type { JobsApiResult } from '@/types/Job'
import type { BranchesApiResult } from '@/types/Branch'
import { client, getRequestOption } from '@/apis/client'

class RepositoryApi {
  getList(params: any | null = null, token: string | null = null): Promise<RepositoriesApiResult> {
    const uri = 'repositories'
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<RepositoriesApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  getOne(repoId: string, token: string | null = null): Promise<Repository> {
    const uri = `repositories/${repoId}`
    const options = getRequestOption(uri, 'get', null, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<Repository>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  create(vals: RepositoryFormVals, token: string | null = null): Promise<Repository> {
    const uri = 'repositories'
    const options = getRequestOption(uri, 'post', null, token)
    return new Promise((resolve, reject) => {
      client
        .post(uri, vals, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }

  update(
    repoId: string,
    vals: RepositoryUpdateFormVals,
    token: string | null = null
  ): Promise<Repository> {
    const uri = `repositories/${repoId}`
    const options = getRequestOption(uri, 'post', null, token)
    return new Promise((resolve, reject) => {
      client
        .put(uri, vals, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }

  getJobs(
    repoId: string,
    params: any | null = null,
    token: string | null = null
  ): Promise<JobsApiResult> {
    const uri = `repositories/${repoId}/jobs`
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<JobsApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  getBranches(
    repoId: string,
    params: any | null = null,
    token: string | null = null
  ): Promise<BranchesApiResult> {
    const uri = `repositories/${repoId}/branches`
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<BranchesApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }
}

export default new RepositoryApi()
