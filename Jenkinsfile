pipeline {
    agent any

    environment {
        REGISTRY = "ghcr.io/itexperts-sanju"      // GitHub Container Registry namespace
        APP_NAME = "myapp"                        // Image/app name
    }

    stages {
        stage('Checkout Repo') {
            steps {
                git url: 'https://github.com/ITexperts-sanju/fullpipeline.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $REGISTRY/$APP_NAME:${BUILD_NUMBER} .'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'ghcr_pat', variable: 'GHCR_PAT')]) {
                    sh '''
                        echo $GHCR_PAT | docker login ghcr.io -u ITexperts-sanju --password-stdin
                        docker push $REGISTRY/$APP_NAME:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Update GitOps Repo') {
            steps {
                withCredentials([string(credentialsId: 'ghcr_pat', variable: 'GHCR_PAT')]) {
                    script {
                        sh '''
                          rm -rf gitops
                          git clone https://ITexperts-sanju:${GHCR_PAT}@github.com/ITexperts-sanju/fullpipeline.git gitops
                          cd gitops

                          # Update deployment.yaml image tag
                          sed -i "s|image:.*|image: $REGISTRY/$APP_NAME:${BUILD_NUMBER}|" deployment.yaml

                          git config user.name "jenkins"
                          git config user.email "jenkins@example.com"
                          git add .
                          git commit -m "Update image to build ${BUILD_NUMBER}"
                          git push origin main
                        '''
                    }
                }
            }
        }
    }
}
