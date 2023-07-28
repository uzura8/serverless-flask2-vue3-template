import type { Auth, User, UserCredential } from '@firebase/auth'
import {
  getAuth,
  onAuthStateChanged,
  //getIdToken,
  signInWithEmailAndPassword,
  signOut
} from 'firebase/auth'
import { initializeApp } from 'firebase/app'
import firebaseConfig from '@/configs/firebase-app-sdk-config.json'

const app = initializeApp(firebaseConfig)

class FirebaseApi {
  getCurrentUser(): User | null {
    const auth: Auth = getAuth(app)
    return auth.currentUser
  }

  onAuthStateChanged(): Promise<User | null> {
    return new Promise((resolve, reject) => {
      try {
        const auth: Auth = getAuth(app)
        onAuthStateChanged(auth, (user) => {
          resolve(user)
        })
      } catch (err) {
        reject(err)
      }
    })
  }

  //async getIdToken(): Promise<string | null> {
  //  const auth: Auth = getAuth(app)
  //  if (auth.currentUser) {
  //    const idToken = await auth.currentUser.getIdToken()
  //    return idToken
  //  }
  //  return null
  //}

  signIn(email: string, password: string): Promise<UserCredential> {
    return new Promise((resolve, reject) => {
      const auth: Auth = getAuth(app)
      signInWithEmailAndPassword(auth, email, password)
        .then((userCredential: UserCredential) => {
          resolve(userCredential)
        })
        .catch((err) => {
          reject(err)
        })
    })
  }

  signOut(): Promise<null> {
    return new Promise((resolve, reject) => {
      const auth: Auth = getAuth(app)
      signOut(auth)
        .then(() => resolve(null))
        .catch((err) => reject(err))
    })
  }
}

export default new FirebaseApi()
