# Создать дополнительный пустой диск

resource "yandex_compute_disk" "secondary" {
  name = var.disk2_name
  type = var.disk2_type
  zone = var.zone_name
  size = var.disk2_size
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
      type     = var.disk_type
      size     = var.disk_size
    }
  }

  secondary_disk {
    disk_id = data.yandex_compute_disk.secondary.id
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.subnet.id
    nat       = var.nat
  }

  metadata = {
    user-data          = "${file("./../.metadata/keys/se/yc_user")}"
    serial-port-enable = 1
  }

depends_on = [
  yandex_compute_disk.secondary
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
  name = var.disk2_name
  depends_on = [
    yandex_compute_disk.secondary
  ]
}

