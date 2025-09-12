pipeline {
    agent any

    environment {
        REGISTRY = "ghcr.io/itexperts-sanju"
        APP_NAME = "myapp"
        GITOPS_REPO = "https://ITexperts-sanju:${GHCR_PAT}@github.com/ITexperts-sanju/fullpipeline.git"
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
                    sh 'echo $GHCR_PAT | docker login ghcr.io -u ITexperts-sanju --password-stdin'
                    sh "docker push $REGISTRY/$APP_NAME:${BUILD_NUMBER}"
                }
            }
        }

        stage('Update GitOps Repo') {
            steps {
                withCredentials([string(credentialsId: 'ghcr_pat', variable: 'GHCR_PAT')]) {
                    script {
                        sh '''
                            rm -rf gitops
                            echo "Cloning GitOps repo..."
                            git clone $GITOPS_REPO gitops

                            # Create k8s folder & default deployment.yaml if missing
                            mkdir -p gitops/k8s
                            if [ ! -f gitops/k8s/deployment.yaml ]; then
                                cat <<EOF > gitops/k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: $REGISTRY/$APP_NAME:latest
        ports:
        - containerPort: 80
EOF
                            fi

                            # Update image tag
                            sed -i "s|image:.*|image: $REGISTRY/$APP_NAME:${BUILD_NUMBER}|" gitops/k8s/deployment.yaml

                            # Commit & push
                            cd gitops
                            git config user.name "jenkins"
                            git config user.email "jenkins@example.com"
                            git add .
                            git commit -m "Update image to build ${BUILD_NUMBER}" || echo "No changes to commit"
                            git push origin main
                        '''
                    }
                }
            }
        }
    }
}
