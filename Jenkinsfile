pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'sudo apt update'
        sh 'sudo apt install python3-pip'
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