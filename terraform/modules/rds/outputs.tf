output "db_instance_endpoint" {
  value       = aws_db_instance.this.endpoint
  description = "RDS endpoint"
}


output "db_instance_id" {
  value       = aws_db_instance.this.id
  description = "RDS instance ID"
}
