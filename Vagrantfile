# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant::Config.run do |config|
  config.vm.box = "precise32"
  config.vm.forward_port 80, 8080

  config.vm.share_folder "v-data", "~/local", "."

  #config.vm.provision :puppet do |puppet|
  #  #puppet.facter = { "fqdn" => "local.pyrocms", "hostname" => "www" }
  #  #puppet.manifests_path = "puppet/manifests"

  #  puppet.manifests_path = "."
  #  puppet.manifest_file  = "django-postgis.pp"
  #  #puppet.module_path  = "puppet/modules"
  #end
end
