pipeline {
    agent { label 'docker-slave' }
    environment {
        // CI-CD vars
        docker_registry_ip = credentials('jenkins-docker-registry-ip')
       // When triggered from git tag, $BRANCH_NAME is actually GIT's tag_name
       TAG_SEM_VER_COMPLIANT = """${sh(
                returnStdout: true,
                script: './resources/CI-CD/validate_tag.sh SemVar $BRANCH_NAME'
            )}"""

       TAG_MAJOR_RELEASE = """${sh(
                returnStdout: true,
                script: './resources/CI-CD/validate_tag.sh MajRel $BRANCH_NAME'
            )}"""

       TAG_PRODUCTION = """${sh(
                returnStdout: true,
                script: './resources/CI-CD/validate_tag.sh production $BRANCH_NAME'
            )}"""

       TAG_STAGING = """${sh(
                returnStdout: true,
                script: './resources/CI-CD/validate_tag.sh staging $BRANCH_NAME'
            )}"""
   }
    stages {
        stage ('Pull repo code from github') {
            steps {
                checkout scm
            }
        }
        stage('Inspect GIT TAG'){
            steps {
                sh """ #!/bin/bash
                echo 'TAG: $BRANCH_NAME'
                echo 'Tag is compliant with SemVar 2.0.0: $TAG_SEM_VER_COMPLIANT'
                echo 'Tag is Major release: $TAG_MAJOR_RELEASE'
                echo 'Tag is production: $TAG_PRODUCTION'
                echo 'Tag is staging: $TAG_STAGING'
                """
            }
        }
        stage('Build monitoring-system-ruleserver') {
            when {
                allOf {
                    // Triggered on every tag, that is considered for staging or production
                    expression{tag "*"}
                    expression{
                        TAG_STAGING == 'true' || TAG_PRODUCTION == 'true'
                    }
                }
             }
            steps {
                sh "cd ruleserver/app/ && ../../resources/CI-CD/make_docker.sh build monitoring-system-ruleserver"
            }
        }
        stage('Push monitoring-system-ruleserver to sodalite-private-registry') {
            // Push during staging and production
            when {
                allOf {
                    expression{tag "*"}
                    expression{
                        TAG_STAGING == 'true' || TAG_PRODUCTION == 'true'
                    }
                }
            }
            steps {
                withDockerRegistry(credentialsId: 'jenkins-sodalite.docker_token', url: '') {
                    sh  """#!/bin/bash
                        ./resources/CI-CD/make_docker.sh push monitoring-system-ruleserver staging
                        """
                }
            }
        }
        stage('Push monitoring-system-ruleserver to DockerHub') {
            when {
                allOf {
                    // Triggered on every tag, that is considered for staging or production
                    expression{tag "*"}
                    expression{
                        TAG_PRODUCTION == 'true'
                    }
                }
             }
            steps {
                withDockerRegistry(credentialsId: 'jenkins-sodalite.docker_token', url: '') {
                    sh "./resources/CI-CD/make_docker.sh push monitoring-system-ruleserver production"
                }
            }
        }
    }
}
