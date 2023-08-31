import type { AxiosResponse, AxiosError } from 'axios'
import type { JobsApiResult, Job } from '@/types/Job'
import { client, getRequestOption } from '@/apis/client'

class JobApi {
  getList(params: any | null = null, token: string | null = null): Promise<JobsApiResult> {
    const uri = 'jobs'
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

  getOne(jobId: string, token: string | null = null): Promise<Job> {
    const uri = `jobs/${jobId}`
    const options = getRequestOption(uri, 'get', null, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<Job>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }
}

export default new JobApi()
