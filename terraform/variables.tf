variable "ya_service_account" {
  description = "Specify service account name for connect to Yandex Cloud"
  type        = string
  default     = "tfadmin"
}

variable "ya_cloud_id" {
  description = "Specify Yandex Cloud ID"
  type        = string
  default     = "b1ga0bs8pioqsr6ck6kk"
}

variable "ya_folder_id" {
  description = "Specify Yandex Cloud project folder ID"
  type        = string
  default     = "b1gsc21jkqe9c22n1abl"
}
