pipeline {
    agent any

    environment {
        DOCKERHUB_CREDS = credentials('dockerhub-creds')
        IMAGE_NAME = "ajith1705/two-tier-app"
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r app/requirements.txt
                    cd app && python -m unittest test_app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKERHUB_CREDS_PSW | docker login -u $DOCKERHUB_CREDS_USR --password-stdin
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to App Server') {
    steps {
        sshagent(credentials: ['app-server-ssh-key']) {
            sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@<app-server-ip> \
                "docker pull ${IMAGE_NAME}:latest && \
                 docker compose -f /home/ubuntu/two-tier-app/docker-compose.yml up -d --no-deps app"
            '''
        }
    }
}

        stage('Verify Deployment') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://13.232.46.104:5000/health || exit 1
                '''
            }
        }
    }

    post {
        failure {
            echo "Pipeline failed — check the stage logs above."
        }
        success {
            echo "Deployed ${IMAGE_TAG} successfully."
        }
    }
}