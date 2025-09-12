pipeline {
    agent any

    environment {
        REGISTRY = "ghcr.io/itexperts-sanju"  // GitHub Container Registry namespace
        APP_NAME = "myapp"                     // Image/app name
        GITOPS_REPO = "https://github.com/ITexperts-sanju/fullpipeline.git"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $REGISTRY/$APP_NAME:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([string(credentialsId: 'ghcr_pat', variable: 'GHCR_PAT')]) {
                    sh """
                        echo $GHCR_PAT | docker login ghcr.io -u ITexperts-sanju --password-stdin
                        docker push $REGISTRY/$APP_NAME:${BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Update GitOps Repo') {
            steps {
                withCredentials([string(credentialsId: 'ghcr_pat', variable: 'GHCR_PAT')]) {
                    script {
                        // Clean old clone
                        sh "rm -rf ${WORKSPACE}/gitops"
                        
                        echo "Cloning GitOps repo..."
                        sh "git clone https://ITexperts-sanju:${GHCR_PAT}@github.com/ITexperts-sanju/fullpipeline.git ${WORKSPACE}/gitops"

                        def deploymentFile = "${WORKSPACE}/gitops/k8s/deployment.yaml"

                        if (fileExists(deploymentFile)) {
                            echo "Updating deployment.yaml with new image..."
                            sh """
                                sed -i 's|image:.*|image: $REGISTRY/$APP_NAME:${BUILD_NUMBER}|' ${deploymentFile}
                                cd ${WORKSPACE}/gitops
                                git config user.name "jenkins"
                                git config user.email "jenkins@example.com"
                                git add .
                                git commit -m "Update image to build ${BUILD_NUMBER}"
                                git push origin main
                            """
                        } else {
                            error "deployment.yaml not found at ${deploymentFile}. Check repo structure."
                        }
                    }
                }
            }
        }
    }
}
