# Получаем значения присвоенных ip-адресов

output "internal_ipaddr_vm01" {
  description = "internal ip 0f VM"
  value       = module.yandex_instance_1.internal_ipaddr_vm
}

output "external_ipaddr_vm01" {
  description = "external ip of VM"
  value       = module.yandex_instance_1.external_ipaddr_vm
}

