variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "public_subnet_az" {
  description = "Availability zone for the public subnet"
  type        = string
}

variable "private_subnet_cidrs" {
  description = "CIDR block for the private subnet"
  type        = list(string)
}

variable "private_subnet_azs" {
  description = "Availability zone for the private subnet"
  type        = list(string)
}

variable "enable_dns_support" {
  description = "Enable DNS support in the VPC"
  type        = bool
  default     = true
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in the VPC"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default     = {
    Owner       = "devops"
  }
}
