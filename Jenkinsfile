pipeline {
    agent any
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
                    poetry install --with test
                    poetry run pytest -vv
                    echo 'Application tested successfully'
                }
            }
        }
    }
}
