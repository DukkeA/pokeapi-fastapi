pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                withCredentials([string(credentialsId: 'token_pokeapi', variable: 'GITHUB_TOKEN')]) {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], 
                    doGenerateSubmoduleConfigurations: false, 
                    extensions: [], 
                    submoduleCfg: [], 
                    userRemoteConfigs: [[
                        credentialsId: 'token_pokeapi', 
                        url: "https://github.com/DukkeA/pokeapi-fastapi.git"
                    ]]])
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo 'Building Docker images'
                    sh 'docker-compose -f compose/with_db/docker-compose.yml build'
                    echo 'Docker images built successfully'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests'
                    sh 'docker-compose -f compose/tests/docker-compose.yml up --build'
                    echo 'Tests completed successfully'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo 'Deploying application'
                    sh 'docker-compose -f compose/with_db/docker-compose.yml up --build -d'
                    echo 'Application deployed successfully'
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker containers
            sh 'docker-compose -f docker-compose.yml down'
        }
    }
}