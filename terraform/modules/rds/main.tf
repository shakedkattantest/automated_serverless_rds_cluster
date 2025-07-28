resource "aws_db_instance" "main" {
  identifier             = "${var.name}-main-db"
  allocated_storage      = var.allocated_storage
  engine                 = var.engine
  instance_class         = var.instance_class
  username               = var.username
  password               = var.password
  db_subnet_group_name   = var.db_subnet_group_name
  vpc_security_group_ids = var.security_group_ids
  publicly_accessible    = false
  skip_final_snapshot     = true

  tags = {
    Name = "${var.name}-main-db"
  }
}

resource "aws_db_instance" "read_replica" {
  identifier           = "${var.name}-replica-db"
  replicate_source_db  = aws_db_instance.main.id
  depends_on          = [aws_db_instance.main]
  instance_class       = var.instance_class  
  publicly_accessible  = false
  skip_final_snapshot  = true

  tags = {
    Name = "${var.name}-replica-db"
  }
}
