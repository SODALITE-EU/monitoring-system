pipeline {
    agent { label 'docker-slave' }
    stages {
        stage ('Pull repo code from github') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker image') {
            steps {
                sh "git fetch --tags && docker build -t sodaliteh2020/monitoring-system ."
            }
        }
        stage('Push image to DockerHub') {
            steps {
                withDockerRegistry(credentialsId: 'jenkins-sodalite.docker_token', url: '') {
                    sh "resources/bin/make_docker.sh push sodaliteh2020/monitoring-system"
                }
            }
        }
    }
}
