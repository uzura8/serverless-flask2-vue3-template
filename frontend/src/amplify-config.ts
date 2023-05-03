import { Amplify } from 'aws-amplify'
import cognitoConfig from './configs/cognito-client-config.json'
Amplify.configure({ Auth: cognitoConfig })
