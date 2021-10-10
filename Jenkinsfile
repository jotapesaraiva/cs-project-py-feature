pipeline {
    agent any
    
    environment {
        AWS_DEFAULT_REGION='us-east-2'
        //THE_BUTLER_SAYS_SO = credentials('Jenkins-aws-creds')
        BUILDNAME='cs-projetct-py-feature-${BUILD_NUMBER}'
        BUCKETNAME='artefactrepository' //S3
        APPLICATIONNAME='pythonTest'  // Elasticbeanstalk
        ENVIRONMENTNAME='Pythontest-env'

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

        stage('Empacotando') {
            steps {
                echo 'Compactando arquivo em ZIP'
                sh"""zip -r ${BUILDNAME}.zip * -x '*venv*'"""
                echo 'removendo o venv'
                sh 'rm -rf venv'
            }
        }

        stage('Archivament S3') {
            steps {
                echo 'Deploying on S3....'
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'Jenkins-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws s3 ls s3://${BUCKETNAME}

                        aws s3 cp ${BUILDNAME}.zip s3://${BUCKETNAME} --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }

        stage('create elasticbeanstalk'){
            steps{
                echo ''
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'Jenkins-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                    aws elasticbeanstalk create-application-version
                    --application-name "${APPLICATIONNAME}"
                    --version-label "${BUILDNAME}"
                    --description "Build created from JENKINS. Job:${JOB_NAME}, BuildId:${BUILD_DISPLAY_NAME}, GitCommit:${GIT_COMMIT,} GitBranch:${GIT_BRANCH}"
                    --source-bundle S3Bucket=${BUCKETNAME},S3Key=${BUILDNAME}.zip
                    --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }

        stage('create elasticbeanstalk'){
            steps{
                echo ''
                withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'Jenkins-aws-creds', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws elasticbeanstalk update-environment
                        --environment-name "${ENVIRONMENTNAME}"
                        --version-label "${BUILDNAME}"
                        --region ${AWS_DEFAULT_REGION}
                    """
                }
            }
        }




    }
}
