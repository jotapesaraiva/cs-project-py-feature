pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION='us-east-1'
        THE_BUTLER_SAYS_SO = credentials('cyn-aws-creds')
        FLASK_ENV = 'testing'
        FLASK_APP = 'application.py'
        DEBUG = true
    }
    stages {
        stage('Git Checkout') {
            steps {

                git branch: env.BRANCH_NAME , url: 'http://gitlab.csicorpnet.com.br/cynthia/cs-project-py.git'
                checkout scm
                
            }
        }
        stage ("Install Dependencies") {
            steps {
                
                /*
                
                pip install virtualenv
                virtual venv
                venv/Scripts/Activate
                */
                sh """
                pip install --upgrade pip
                pip install -r ${env.WORKSPACE}/requirements.txt
                """
            }
        }
        stage('Run Tests') {
            steps {
                //venv/Scripts/activate
                sh """
                echo "Running the unit test..."
                make clean
                make coverage
                """
            }
        }
        stage('Generate Release and deploy') {
            steps {
                script {
                    def version = readFile encoding: 'utf-8', file: '__version__.py'
                    def message = "Latest ${version}. New version:"
                    def releaseInput = input(
                        id: 'userInput',
                        message: "${message}",
                        parameters: [
                            [
                                $class: 'TextParameterDefinition',
                                defaultValue: 'uat',
                                description: 'Release candidate',
                                name: 'rc'
                            ]
                        ]
                    )
                    //venv/Scripts/activate
                    sh """
                    make release v=${releaseInput}
                    fab -H ${env.THE_BUTLER_SAYS_SO} deploy --tag ${releaseInput}
                    """
                }
            }
        }
        /*
        stage('Build') {
            steps {

                echo 'Criando requirements.txt.'
                sh{'''
                    python3.8 -m pip freeze > requirements.txt
                    python3.8 -m pip install -r requirements.txt
                    '''}
                echo 'Instalando requirements.txt'

                //echo 'Installing Maven...'
                //sh "mvn install"

                git branch: env.BRANCH_NAME, credentialsId: '7fceccfd-9ddd-45e5-bea4-e02bb545bf2d', url: 'http://gitlab.csicorpnet.com.br/cynthia/cs-project-py.git'
            }
        }
        */
        /*
        stage('Deploy') {
            agent any
            environment{
                AWS_DEFAULT_REGION='us-east-1'
                THE_BUTLER_SAYS_SO=credentials('cyn-aws-creds') 
            }
            steps {
                echo 'Deploying....'
                sh '''
                    aws --version 
                    aws ec2 describe-instances 
                ''' 
            }
        }
        */
    }
}