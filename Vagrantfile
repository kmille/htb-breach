# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/buster64"
  config.vm.network "public_network"
  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.provider "virtualbox" do |vb|
     vb.memory = "1024"
  end
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "deploy.yaml"
    ansible.become = true
    ansible.extra_vars = { ansible_python_interpreter:"/usr/bin/python3" }
    ansible.ask_vault_pass = true
  end
end

