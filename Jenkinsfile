pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'apt update'
        sh 'apt install python3-pip'
        sh 'pip install -r requirements.txt'
      }
    }
    stage('run') {
      steps {
        sh 'python main.py'
      }   
    }
  }
}