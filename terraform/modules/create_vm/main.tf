# Создать дополнительный пустой диск

resource "yandex_compute_disk" "secondary" {
  count = var.is_second_disk ? 1 : 0 # выполнять только если установлена опция создания второго диска
  name = var.disk2_name
  type = var.disk2_type
  zone = var.zone_name
  size = var.disk2_size
}

resource "yandex_vpc_address" "external" {
  count = var.is_ex_static_ipv4 ? 1 : 0 # выполняется только если установлена опция резервировать внешний статический ip
  name = var.ex_ipv4_name
  external_ipv4_address {
    zone_id = var.zone_name
  }
}

# Создать виртуальную машину с заданным образом

resource "yandex_compute_instance" "vm" {
  description        = var.instance_description
  name               = var.instance_name
  platform_id        = var.platform
  service_account_id = data.yandex_iam_service_account.user_id.id
  zone               = var.zone_name

  resources {
    cores         = var.cores
    memory        = var.memory
    core_fraction = var.core_fract
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.img.id
      name     = var.disk_name
      type     = var.disk_type
      size     = var.disk_size
    }
  }

  dynamic "secondary_disk" {
    for_each = var.is_second_disk ? [1] : []
    content {
      disk_id = data.yandex_compute_disk.secondary[0].id
    }
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.subnet.id
    nat       = var.nat
    nat_ip_address = var.is_ex_static_ipv4 ? data.yandex_vpc_address.external[0].external_ipv4_address[0].address : null # задается только если установлена опция резервирования статического ip
  }

  metadata = {
    user-data          = "${file("./../.metadata/keys/se/yc_user")}"
    serial-port-enable = 1
  }

depends_on = [
  yandex_compute_disk.secondary,
  yandex_vpc_address.external
]
}

# Получить id требуемого образа

data "yandex_compute_image" "img" {
  family = var.instance_family_image
}

#Получить id подсети для инстанса

data "yandex_vpc_subnet" "subnet" {
  name = var.instance_subnet_name
}

# Получить id сервисного аккаунта

data "yandex_iam_service_account" "user_id" {
  name = "se"
}

# Получить id второго диска

data "yandex_compute_disk" "secondary" {
  count = var.is_second_disk ? 1 : 0 # выполнять только если установлена опция создания второго диска
  name = var.disk2_name
  depends_on = [
    yandex_compute_disk.secondary
  ]
}

data "yandex_vpc_address" "external" {
  count = var.is_ex_static_ipv4 ? 1 : 0 # блок выполняется только если установлена опция резервирования внешнего ip
  name = var.ex_ipv4_name
  depends_on = [
    yandex_vpc_address.external
  ]
}



