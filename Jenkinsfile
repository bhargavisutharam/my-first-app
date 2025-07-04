pipeline {
    agent any
    stages {
        stage('Clone source code') {
            steps{
                git branch: 'master', url: https://github.com/bhargavisutharam/my-first-app
            }
        }
        stage('Testing'){
            steps{
                echo 'this is just testing...'
            }
        }
    }
}