variable "name" {
  description = "Name prefix for RDS resources"
  type        = string
}


variable "engine" {
  description = "Database engine (MySQL or PostgreSQL)"
  type        = string
}


variable "engine_version" {
  description = "Engine version"
  type        = string
}


variable "instance_class" {
  description = "Instance class (e.g., db.t3.micro)"
  type        = string
}


variable "allocated_storage" {
  description = "Storage size in GB"
  type        = number
}


variable "db_name" {
  description = "Initial database name"
  type        = string
}


variable "username" {
  description = "Master DB username"
  type        = string
}


variable "password" {
  description = "Master DB password"
  type        = string
  sensitive   = true
}


variable "subnet_ids" {
  description = "List of private subnet IDs for RDS subnet group"
  type        = list(string)
}


variable "vpc_id" {
  description = "VPC ID to associate security group with"
  type        = string
}


variable "security_group_ids" {
  description = "Security group IDs to assign to the RDS instance"
  type        = list(string)
}
