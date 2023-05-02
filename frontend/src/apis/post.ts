import type { AxiosResponse, AxiosError } from 'axios'
import type { PostPublic, PostsApiResult } from '@/types/Post'
import { client, getRequestOption } from './client'

class PostApi {
  getList(serviceId: string, params = {}, token = ''): Promise<PostsApiResult> {
    const uri = `posts/${serviceId}`
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<PostsApiResult>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }

  getOne(serviceId: string, slug: string, params = {}, token = ''): Promise<PostPublic> {
    const uri = `posts/${serviceId}/${slug}`
    const options = getRequestOption(uri, 'get', params, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<PostPublic>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }
}

export default new PostApi()
