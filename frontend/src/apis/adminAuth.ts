import type { CognitoUser } from 'amazon-cognito-identity-js'
import '@/amplify-config'
import { Auth } from 'aws-amplify'

class AdminAuthApi {
  currentAuthenticatedUser(): Promise<CognitoUser> {
    return new Promise((resolve, reject) => {
      Auth.currentAuthenticatedUser()
        .then((user: CognitoUser) => {
          resolve(user)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }

  signIn(email: string, password: string): Promise<CognitoUser> {
    return new Promise((resolve, reject) => {
      Auth.signIn(email, password)
        .then((user: CognitoUser) => {
          resolve(user)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }

  signOut(): Promise<null> {
    return new Promise((resolve, reject) => {
      Auth.signOut()
        .then((res) => {
          resolve(res)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }
}

export default new AdminAuthApi()
