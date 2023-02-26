# Создание ВМ с помощью модуля

module "yandex_instance_1" {
  source                = "./modules/create_vm"
  disk_size             = "25"
  disk_type             = "network-ssd"
  disk_name             = "sys"
  is_second_disk        = "false"
  disk2_size            = "60"
  disk2_type            = "network-ssd"
  disk2_name            = "data"
  cores                 = "2"
  memory                = "4"
  core_fract            = "50"
  instance_family_image = "centos-7"
  instance_subnet_name  = "default-ru-central1-a"
  instance_name         = "test"
  instance_description  = "test VM for findconf project"
  zone_name             = "ru-central1-a"
  is_ex_static_ipv4     = false # внешний ip был зарезервирован вручную
  ex_ipv4_name          = "ex-ip-test"
}
