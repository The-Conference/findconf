terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.82.0"
    }
  }

  required_version = ">= 0.13"
}

provider "yandex" {
  service_account_key_file = file("./../.metadata/keys/tfadmin/authorized_key.json")
  cloud_id                 = var.ya_cloud_id
  folder_id                = var.ya_folder_id
  zone                     = "ru-central1-a"
}

