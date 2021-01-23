### breach.htb
This is the source code of the [Hack The Box](https://www.hackthebox.eu/) challenge breach. The solution and exploit will be published in this repo after the box is retired.

Some hints:
- you don't have to brute force passwords at any stage of this box
- to solve this box it might be helpful to run the box on your own machine
- this repo contains an Ansible playbook. The privilege escalation part in `tasks/post.yaml` is encrypted with vault. The password will also be released in the future
- the box was tested on Debian buster (1 CPU/1GB RAM is fine)
- the plan is to make an IppSec like video in the future. It will be linked here in the repo


### How to run the playbook
option A: use the vagrant file
```
vagrant up
vagrant ssh
sudo -s
```
If you don't have the vault password, change `ansible.ask_vault_pass` to `false`  in the `Vagrantfile` and comment out the line  `- import_tasks: tasks/post.yaml` in `deploy.yaml`.

option B: run it directly. You have to add a manual ssh config entry for a machine called `breach.htb`.

with the Vault password, use
`ansible-playbook --ask-vault-pass deploy.yaml`
without the Vault password, comment out  the `- import_tasks: tasks/post.yaml` line in `deploy.yaml` and run
`ansible-playbook deploy.yaml`

Deploy flags with
`ansible-playbook --ask-vault-pass deploy.yaml --extra-vars=user_token=thisistheusertoken --extra-vars=root_token=thisistheroottoken`

You can change the ip of the box without breaking anything. For feedback or bugs contact [kmille](https://twitter.com/kmille_____).
