pipeline {
  agent any
  environment {
    registry = "arshd/web_app"
    registryCredential = 'dockerhub'
    dockerImage = ''
  }
  stages {
    // stage('init'){
    //     def dockerHome = tool 'mydocker'
    //     env.PATH = "${dockerHome}/bin:${env.PATH}"
    // }
    stage('build') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
    // stage('building Image') {
    //   steps {
    //     script {
    //         dockerImage = docker.build registry + ":$BUILD_NUMBER"
    //     }
    //   }   
    // }
    // stage('Deploy Image'){
    //     steps{
    //         script{
    //             docker.withRegistry('', registryCredential) {
    //                 dockerImage.push()
    //            }
    //         }
    //     }
    // }
  }
}