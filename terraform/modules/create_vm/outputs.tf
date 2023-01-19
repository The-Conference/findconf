output "internal_ipaddr_vm" {
  description = "internal ip 0f VM"
  value       = yandex_compute_instance.vm.network_interface.0.ip_address
}

output "external_ipaddr_vm" {
  description = "external ip of VM"
  value       = yandex_compute_instance.vm.network_interface.0.nat_ip_address
}

output "vpc_subnet" {
  description = "id of instances subnet"
  value       = yandex_compute_instance.vm.network_interface.0.subnet_id
}
