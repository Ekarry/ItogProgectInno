#!/bin/bash
set -x
sudo apt-get update -y
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible -y
sudo apt-get install -y git ansible
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub
git config --global user.name "Ekaterina Dmitrieva"
git config --global user.email "ekarry@yandex.ru"

mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.285.1.tar.gz -L https://github.com/actions/runner/releases/download/v2.285.1/actions-runner-linux-x64-2.285.1.tar.gz
echo "5fd98e1009ed13783d17cc73f13ea9a55f21b45ced915ed610d00668b165d3b2  actions-runner-linux-x64-2.285.1.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.285.1.tar.gz

echo 'You need configure GitHub-runner'
echo 'Select the repository.'
echo 'Setting -> Actions -> Runners -> New self-hosted runner -> Linux'
echo 'Run the commands from the Configure section'

echo 'git clone git@github.com:BanLex/final.git'
