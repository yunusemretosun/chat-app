pipeline{
    agent any

    environment{
        DOCKERHUB_USERNAME = "yunusemretosun"
        APP_NAME = "chatapp"
        IMAGE_TAG = "${BUILD_NUMBER}"
        IMAGE_NAME = "${DOCKERHUB_USERNAME}"+"/"+"${APP_NAME}"
        REGISTRY_CREDS = "dockerhub"
    }

    stages{
        stage("Clean workspace"){
            steps{
                script{
                    cleanWs()
                }
            }
        }

        stage("Checkout SCM"){
            steps{
                script{
                    git credentialsId: 'github',
                    url: 'https://github.com/yunusemretosun/chat-app.git',
                    branch: "main"
                }
            }
        }

        stage("Build Docker Image"){
            steps{
                script{
                    docker_image = docker.build "${IMAGE_NAME}"
                }
            }
        }

        stage("Push Docker Image"){
            steps{
                script{
                    docker.withRegistry("",REGISTRY_CREDS){
                        docker_image.push("${BUILD_NUMBER}")
                        docker_image.push("latest")
                        }
                }
            }
        }

        stage("Delete Docker Image"){
            steps{
                script{
                    
                    sh "docker rmi ${IMAGE_NAME}:${IMAGE_TAG}"
                    sh "docker rmi ${IMAGE_NAME}:latest"
                    }
                }
            }

        stage("Updateing Openshift Deployment Files"){
            steps{
                script{
                    
                    sh """
                        cat /openshift/capp-deployment.yaml
                        sed -i 's/${APP_NAME}.*/${APP_NAME}:${IMAGE_TAG}/g' /openshift/capp-deployment.yaml
                        cat /openshift/capp-deployment.yaml
                    """
                    }
                }
            }

        stage("Push the changed files to github"){
            steps{
                script{
                    
                    sh """
                        git config --global user.email "yunusemre.tosun@sekom.com.tr"
                        git config --global user.name "yunusemretosun"
                        git add /openshift/capp-deployment.yaml
                        git commit -m "changed deployment file"
                    """ 
                    withCredentials([gitUsernamePassword(credentialsId: 'github', gitToolName: 'Default')]) {
                            sh "git push  https://github.com/yunusemretosun/chat-app.git main" 
                        }
                    }
                }
            }
            
    }
}