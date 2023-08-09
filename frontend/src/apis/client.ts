import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import type { ApiParams } from '@/types/Common'
import { config } from '@/configs'

const client: AxiosInstance = axios.create({
  baseURL: config.api.origin + config.api.basePath,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json'
  },
  //withCredentials: true,
  responseType: 'json'
})

const getRequestOption = (
  url: string,
  method: string,
  params: ApiParams | null = null,
  token: string | null = null,
  isAdmin: boolean = false
) => {
  const params_cloned = { ...params }
  const options: AxiosRequestConfig = {
    url: url,
    method: method.toUpperCase(),
    params: params_cloned
  }
  if (token) {
    const headerName = isAdmin ? config.api.authHeader.admin.name : config.api.authHeader.user.name
    const tokenPrefix = isAdmin
      ? config.api.authHeader.admin.tokenPrefix
      : config.api.authHeader.user.tokenPrefix
    const headerValue = [tokenPrefix, token].join(' ')
    options.headers = { [headerName]: headerValue }
  }
  return options
}

export { client, getRequestOption }
