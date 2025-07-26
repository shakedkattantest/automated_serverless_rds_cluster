resource "aws_db_instance" "this" {
  identifier             = "${var.name}-db"
  allocated_storage      = var.allocated_storage
  engine                 = var.engine
  engine_version         = var.engine_version
  instance_class         = var.instance_class
  name                   = var.db_name
  username               = var.username
  password               = var.password
  subnet_ids             = var.subnet_ids
  vpc_security_group_ids = var.security_group_ids
  skip_final_snapshot    = true
  publicly_accessible    = false

  tags = {
    Name = "${var.name}-db"
  }
}
