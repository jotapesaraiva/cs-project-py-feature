pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION='us-east-1'
        //THE_BUTLER_SAYS_SO = credentials('Jenkins-aws-creds')
        FLASK_ENV = 'testing'
        FLASK_APP = 'application.py'
        DEBUG = true
    }
    stages {
        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Init'){
            steps{
                //checkout scm;
                script{
                env.BASE_DIR = pwd()
                env.CURRENT_BRANCH = env.BRANCH_NAME
                env.IMAGE_TAG = getImageTag(env.CURRENT_BRANCH)
                env.TIMESTAMP = getTimeStamp();
                env.APP_NAME= getEnvVar('APP_NAME')
                }
            }
        }
        stage ("Install Dependencies") {
            steps {
                sh """
                pip install virtualenv
                virtual venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install flask
                pip install -r requirements.txt
                """
            }
/*        }
        stage('Checkout') {
            steps {
                //venv/Scripts/activate
                sh """
                echo "Verificação de Dependencies"
                pip list
                which pip
                which python
                """
            }
        }*/
        stage('test') {
            steps {
                sh 'python test.py'
            }
            post {
                always {junit 'test-reports/*.xml'}
            }
        }
/*        stage('Generate Release and deploy') {
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
        }*/

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
