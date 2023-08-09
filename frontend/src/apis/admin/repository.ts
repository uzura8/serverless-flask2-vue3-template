import type { AxiosResponse, AxiosError } from 'axios'
import type { RepositoryApiResult, Repository, RepositoryFormVals } from '@/types/Repository'
import { client, getRequestOption } from '@/apis/client'

class AdminRepositoryApi {
  getList(params: any | null = null, token: string | null = null): Promise<RepositoryApiResult> {
    const uri = 'admin/repositories'
    const options = getRequestOption(uri, 'get', params, token, true)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<RepositoryApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  getOne(repoId: string, token: string | null = null): Promise<Repository> {
    const uri = `admin/repositories/${repoId}`
    const options = getRequestOption(uri, 'get', null, token, true)
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
    const uri = 'admin/repositories'
    const options = getRequestOption(uri, 'post', null, token, true)
    return new Promise((resolve, reject) => {
      client
        .post(uri, vals, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }

  update(
    repoId: string,
    vals: RepositoryFormVals,
    token: string | null = null
  ): Promise<Repository> {
    const uri = `admin/repositories/${repoId}`
    const options = getRequestOption(uri, 'post', null, token)
    return new Promise((resolve, reject) => {
      client
        .put(uri, vals, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }
}

export default new AdminRepositoryApi()
