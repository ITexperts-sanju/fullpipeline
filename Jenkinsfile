pipeline {
    agent any

    environment {
        REGISTRY = "ghcr.io/itexperts-sanju"
        APP_NAME = "myapp"
        GITOPS_REPO = "https://ITexperts-sanju:${GHCR_PAT}@github.com/ITexperts-sanju/fullpipeline.git"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Unit Tests') {
            steps {
                echo "Running Python Unit Tests..."
                sh '''
                    mkdir -p reports
                    if [ -f requirements.txt ]; then
                        pip install --no-cache-dir -r requirements.txt
                    fi
                    pip install --no-cache-dir pytest
                    pytest tests --maxfail=1 --disable-warnings --junitxml=reports/unit_tests.xml || true
                '''
            }
            post {
                always {
                    junit 'reports/unit_tests.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t $REGISTRY/$APP_NAME:${BUILD_NUMBER} ."
                }
            }
        }

        stage('Trivy Vulnerability Scan') {
            steps {
                echo "Running Trivy Scan..."
                sh '''
                    mkdir -p reports
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        -v $WORKSPACE:/project \
                        aquasec/trivy image --format json --output reports/trivy_report.json $REGISTRY/$APP_NAME:${BUILD_NUMBER}
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/trivy_report.json', allowEmptyArchive: true
                }
            }
        }

        stage('SonarQube Scan') {
            steps {
                echo "Running SonarQube Analysis..."
                withCredentials([string(credentialsId: 'sonar_token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        docker run --rm \
                          -e SONAR_HOST_URL=http://host.docker.internal:9000 \
                          -e SONAR_LOGIN=$SONAR_TOKEN \
                          -v $WORKSPACE:/usr/src \
                          sonarsource/sonar-scanner-cli \
                          -Dsonar.projectKey=myapp \
                          -Dsonar.sources=. \
                          -Dsonar.python.coverage.reportPaths=reports/unit_tests.xml
                    '''
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
                    sh '''
                        rm -rf gitops
                        git clone $GITOPS_REPO gitops
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
                        sed -i "s|image:.*|image: $REGISTRY/$APP_NAME:${BUILD_NUMBER}|" gitops/k8s/deployment.yaml
                        cd gitops
                        git config user.name "jenkins"
                        git config user.email "jenkins@example.com"
                        git add .
                        git commit -m "Update image to build ${BUILD_NUMBER}" || echo "No changes to commit"
                        git push https://ITexperts-sanju:${GHCR_PAT}@github.com/ITexperts-sanju/fullpipeline.git
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Sending email..."
            mail to: 'sanjay.saregama@gmail.com',
                 subject: "Jenkins Pipeline - ${currentBuild.fullDisplayName}",
                 body: """Pipeline status: ${currentBuild.currentResult}

View details at: ${env.BUILD_URL}
"""
        }
    }
}
