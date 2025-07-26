resource "aws_db_instance" "this" {
  identifier             = "${var.name}-db"
  allocated_storage      = var.allocated_storage
  engine                 = var.engine
  instance_class         = var.instance_class
  name                   = var.db_name
  username               = var.username
  password               = var.password
  db_subnet_group_name   = var.db_subnet_group_name
  vpc_security_group_ids = var.security_group_ids
  publicly_accessible    = false

  tags = {
    Name = "${var.name}-db"
  }
}
