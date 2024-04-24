pipeline {
    agent any

    environment{
        DEBUG="true"
        LOG_LEVEL="INFO"
        DB_USER="test"
        DB_PASSWORD="test"
        DB_HOST="postgres"
        DB_PORT="5432"
        DB_NAME="pokemon_db"
    }

    stages {

        stage('Prepare environment') {
            steps {
                script {
                    echo 'Preparing environment'
                    sh 'python3 --version'
                    sh 'pip3 --version'
                    sh 'poetry --version'
                }
            }
        }

        stage('Configure DB') {
            steps {
                script {
                    writeFile file: '.env', text: """
                    DEBUG="true"
                    LOG_LEVEL="INFO"
                    DB_USER="test"
                    DB_PASSWORD="test"
                    DB_HOST="postgres"
                    DB_PORT="5432"
                    DB_NAME="pokemon_db"
                    """
                }
            }
        }

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

        stage('Test') {
            steps {
                script {
                    echo 'Testing application'
                    sh 'poetry install --with test'
                    sh 'poetry run pytest -vv'
                    echo 'Application tested successfully'
                }
            }
        }
    }
}
