Vagrant.configure("2") do |config|
    config.vm.define "ares" do |ares|
        # Template for virtualbox to be used
        ares.vm.box = "debian/jessie64"
        # Check for updates regularly
        ares.vm.box_check_update = true
        # Domain
        ares.vm.hostname = "ares.dev"
        # Forward neo4j port so it will be accesible from localhost
	ares.vm.network :forwarded_port, guest: 7474, host: 7474	
        ares.vm.network "forwarded_port", guest: 7687, host: 7687
        # Tell vagrant to run ansible as a provisioner
        ares.vm.provision "ansible" do |ansible|
            # make verbose output
	    ansible.verbose = "v"
	    # where is the playbook located
            ansible.playbook = "ansible/playbook.yml"
        end
    end
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory on the VM:
    vb.memory = 2048
    vb.cpus = 2
  end
end
