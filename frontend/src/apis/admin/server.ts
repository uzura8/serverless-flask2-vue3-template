import type { AxiosResponse, AxiosError } from 'axios'
import type { Server, ServersApiResult, ServerDeployStatusForRequest } from '@/types/Server'
import { client, getRequestOption } from '@/apis/client'

class AdminServerApi {
  getList(params: any | null = null, token: string | null = null): Promise<ServersApiResult> {
    const uri = 'admin/servers'
    const options = getRequestOption(uri, 'get', params, token, true)
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
    const uri = `admin/servers/${domain}`
    const options = getRequestOption(uri, 'get', null, token, true)
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
    const uri = `admin/servers/${domain}/deploy/${status}`
    const options = getRequestOption(uri, 'put', null, token)
    return new Promise((resolve, reject) => {
      client
        .put(uri, null, options)
        .then((res) => resolve(res.data))
        .catch((err) => reject(err))
    })
  }
}

export default new AdminServerApi()
