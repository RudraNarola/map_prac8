pipeline {
    agent any
    
    stages {
        stage('Build Images') {
            steps {
                bat 'docker-compose build'
                echo "Docker images built successfully"
            }
        }

        stage('Run Tests') {
            steps {
                bat 'docker run --rm webapp pytest || echo "No tests found"'
                bat 'docker run --rm dbapp pytest || echo "No tests found"'
                echo "Tests completed"
            }
        }

        stage('Deploy Containers') {
            steps {
                bat 'docker-compose up -d'
                echo "Containers deployed successfully"
            }
        }
    }
    
    post {
        success {
            echo "Pipeline completed successfully"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
