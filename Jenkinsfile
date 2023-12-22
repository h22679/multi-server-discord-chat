pipeline {
    agent any

    stages {
        stage('Update Repository') {
            steps {
                dir('/apps/msdc') {
                    sh 'git config --global --add safe.directory /apps/msdc'
                    sh 'git rev-parse --is-inside-work-tree || git init'
                    sh 'git remote add origin https://github.com/h22679/multi-server-discord-chat || git remote set-url origin https://github.com/h22679/multi-server-discord-chat'

                    // Fetch and reset without affecting the 'data' directory
                    sh 'git fetch origin'
                    sh 'git reset --hard origin/main'
                    sh 'git clean -fdx --exclude=data'
                }
            }
        }
        stage('Update Requirements') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: 'home', transfers: [sshTransfer(execCommand: "docker exec jenkins_msdc_1 pip install -r /app/requirements.txt")])])
            }
        }
        stage('Restart Bot Container') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: 'home', transfers: [sshTransfer(execCommand: "docker restart jenkins_msdc_1")])])
            }
        }
    }
}
