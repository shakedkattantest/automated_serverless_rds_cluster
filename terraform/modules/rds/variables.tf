variable "name" {
  description = "Name prefix for RDS resources"
  type        = string
}


variable "engine" {
  description = "Database engine (MySQL or PostgreSQL)"
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


variable "username" {
  description = "Master DB username"
  type        = string
}


variable "password" {
  description = "Master DB password"
  type        = string
  sensitive   = true
}


variable "db_subnet_group_name" {
  description = "Name of the DB subnet group to associate with the RDS instance"
  type        = string
}


variable "security_group_ids" {
  description = "Security group IDs to assign to the RDS instance"
  type        = list(string)
}
