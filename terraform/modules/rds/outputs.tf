output "db_instance_endpoint" {
  value       = aws_db_instance.main.endpoint
  description = "RDS endpoint"
}


output "db_instance_id" {
  value       = aws_db_instance.main.id
  description = "RDS instance ID"
}
