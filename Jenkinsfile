pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                dir('/apps/msdc') {
                    sh 'rm -rf *'
                    sh 'git clone https://github.com/h22679/multi-server-discord-chat .'
                }
            }
        }
        stage('Update Requirements') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: 'home', transfers: [sshTransfer(execCommand: "docker exec jenkins_msdc_1 pip install -r ./requirements.txt")])])
            }
        }
        stage('Restart Bot Container') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: 'home', transfers: [sshTransfer(execCommand: "docker restart jenkins_msdc_1")])])
            }
        }
    }
}
