pipeline {
    agent any
    environment {
        HUB = "tarrott"
        IMAGE_REPO = "academy"
        VERSION = "${BUILD_NUMBER}-${GIT_COMMIT}"
        IMAGE = "${IMAGE_REPO}:${VERSION}"
    }
    stages {
        stage('Build container') {
            steps {
                sh "docker build -t ${IMAGE_REPO} ."
            }
        }

        stage('Test') {
            steps {
                sh "echo 'run tests here' "
            }
        }

        stage('Push') {
            when { branch 'develop' }
            steps {
                sh "docker tag ${IMAGE_REPO}:latest ${HUB}/${IMAGE}"
                sh "docker push ${HUB}/${IMAGE_REPO}:latest"
                sh "docker push ${HUB}/${IMAGE}"
            }
        }

        stage('Deploy django') {
            when { branch 'develop' }
            steps {
                sh "ansible-playbook deploy-django.yml"
            }
        }

        stage('Deploy nginx') {
            when { branch 'develop' }
            steps {
                sh "ansible-playbook deploy-nginx.yml"
            }
        }
    }
}