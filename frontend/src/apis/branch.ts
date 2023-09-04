import type { AxiosResponse, AxiosError } from 'axios'
import type { Branch, BranchesApiResult } from '@/types/Branch'
import { client, getRequestOption } from '@/apis/client'

class BranchApi {
  getList(params: any | null = null, token: string | null = null): Promise<BranchesApiResult> {
    const uri = 'branches'
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

  getOne(branchId: string, token: string | null = null): Promise<Branch> {
    const uri = `branches/${branchId}`
    const options = getRequestOption(uri, 'get', null, token)
    return new Promise((resolve, reject) => {
      client(options)
        .then((res: AxiosResponse<Branch>) => {
          resolve(res.data)
        })
        .catch((err: AxiosError<{ error: string }>) => {
          reject(err)
        })
    })
  }
}

export default new BranchApi()
