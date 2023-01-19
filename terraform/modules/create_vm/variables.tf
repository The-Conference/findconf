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

variable "instance_family_image" {
  description = "Specify Image family for Instance"
  type        = string
  default     = "centos-7"
}

variable "instance_subnet_name" {
  description = "Specify name of subnet for creating instance"
  type        = string
  default     = "default-ru-central1-a"
}

variable "instance_name" {
  description = "Specify name of creating instance"
  type        = string
}

variable "instance_description" {
  description = "Specify description for creating instance"
  type        = string
  default     = "no description"
}

variable "zone_name" {
  description = "Specify availability zone for VM"
  type        = string
  default     = "ru-central1-a"
}

variable "nat" {
  description = "Must have the VM external IP"
  type        = bool
  default     = true
}

variable "platform" {
  description = "Specify Compute resource platform"
  type        = string
  default     = "standard-v3"
}

variable "disk_size" {
  description = "set size of the boot disk in GB"
  type        = string
  default     = "25"
}

variable "disk_type" {
  description = "set type of creating disk"
  type        = string
  default     = "network-ssd"
}

variable "disk2_size" {
  description = "set size of the boot disk in GB"
  type        = string
  default     = "60"
}

variable "disk2_type" {
  description = "set type of creating disk"
  type        = string
  default     = "network-ssd"
}

variable "cores" {
  description = "number of virtual cores"
  type        = string
  default     = "2"
}

variable "memory" {
  description = "virtual memory in GB"
  type        = string
  default     = "2"
}

variable "core_fract" {
  description = "core fraction in %"
  type        = string
  default     = "20"
}