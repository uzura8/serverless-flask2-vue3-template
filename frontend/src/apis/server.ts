import type { AxiosResponse, AxiosError } from 'axios'
import type { Server, ServersApiResult, ServerDeployStatusForRequest } from '@/types/Server'
import type { RepositoryApiResult } from '@/types/Repository'
import { client, getRequestOption } from '@/apis/client'

class ServerApi {
  getList(params: any | null = null, token: string | null = null): Promise<ServersApiResult> {
    const uri = 'servers'
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<ServersApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  getOne(domain: string, token: string | null = null): Promise<Server> {
    const uri = `servers/${domain}`
    const options = getRequestOption(uri, 'get', null, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<Server>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  updateDeployStatus(
    domain: string,
    status: ServerDeployStatusForRequest,
    token: string | null = null
  ): Promise<Server> {
    const uri = `servers/${domain}/deploy/${status}`
    const options = getRequestOption(uri, 'put', null, token)
    return new Promise((resolve, reject) => {
      client
        .put(uri, null, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }

  getRepos(
    serverDomain: string,
    params: any | null = null,
    token: string | null = null
  ): Promise<RepositoryApiResult> {
    const uri = `servers/${serverDomain}/repositories`
    const options = getRequestOption(uri, 'get', params, token)
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
}

export default new ServerApi()
