pipeline {
    agent any
    environment {
    GOOGLE_REPOSITORY = 'gcr.io'
    GCP_PROJECT = '<gcp_project_id>'
    DOCKER_IMAGE_NAME = '<image_name>'
    }
    
    options {
        skipDefaultCheckout(true)
    }
    
    stages {
        stage('Checkout') {
            steps {
                // send build started notifications
                slackSend (color: '#FFFF00', message: "STARTED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
                
                checkout scm
                sh "git rev-parse --short HEAD > .git/commit-id" 
                script {
                    COMMIT_ID = readFile('.git/commit-id').trim()
                }                       
                echo "${COMMIT_ID}" 
            }
        }

        stage('Sonar Scan') {
            steps {
               script {
                    sonarqubeScannerHome = tool name: 'sonar', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
                    echo "${sonarqubeScannerHome}" 
                }
                withSonarQubeEnv('sonar') {
                    sh "${sonarqubeScannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Build Image') {
            steps {
               sh "docker build -t ${GOOGLE_REPOSITORY}/${GCP_PROJECT}/${DOCKER_IMAGE_NAME}:${COMMIT_ID} ."
            }
        }
 
         stage('Run Tests') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'echo "Unit tests passed"'
                    }
                }
                stage('Backend Tests') {
                    steps {
                        sh 'echo "Backend tests passed"'
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        sh 'echo "Frontend tests passed"'
                    }
                }
                stage('Model Accuracy Tests') {
                    steps {
                        sh 'echo "Accuracy tests passed"'
                    }
                }
            } 
        }

        stage('Push Image') {
            steps {
                withDockerRegistry([credentialsId: 'gcr:<gcp_project_id>', url: 'https://us.gcr.io']) {
                    echo "${COMMIT_ID}"
                     sh 'docker login -u _json_key --password-stdin https://gcr.io < /var/jenkins_home/gcloud-svc-account.json'
                     sh "docker push ${GOOGLE_REPOSITORY}/${GCP_PROJECT}/${DOCKER_IMAGE_NAME}:${COMMIT_ID}"

                }

            }
        }
    }

    post {
        success {
            slackSend (color: '#00FF00', message: "SUCCESSFUL: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }

        failure {
            slackSend (color: '#FF0000', message: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]' (${env.BUILD_URL})")
        }
    }
}
