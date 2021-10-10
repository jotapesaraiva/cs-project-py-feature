pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION='us-east-2'
        //THE_BUTLER_SAYS_SO = credentials('Jenkins-aws-creds')
        FLASK_ENV = 'testing'
        FLASK_APP = 'application.py'
        DEBUG = true

        BucketName='artefactrepository'
    }
    stages {
        stage('Git Checkout') {
            steps {
                checkout scm
            }
        }
/*        stage('Init'){
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
        }*/
        stage ("Install Dependencies") {
            steps {
                sh """
                /usr/local/bin/virtualenv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install flask
                pip install -r requirements.txt
                """
            }
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

        stage('Empacotando') {
            steps {
                echo 'Compactando arquivo em ZIP'
                sh"""zip -r cs-projetct-py-feature-${BUILD_NUMBER}.zip * -x '*venv*'"""
                echo 'removendo o venv'
                sh 'rm -rf venv'
            }
        }


        stage('Archivament S3') {
            steps {
                echo 'Deploying on S3....'
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'Jenkins-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws s3 cp cs-projetct-py-feature-${BUILD_NUMBER}.zip s3://$BucketName --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }

    }
}
