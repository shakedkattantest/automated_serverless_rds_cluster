module "dev_vpc" {
  source = "git::https://github.com/shakedkattan/automated_serverless_rds_cluster.git///terraform/modules/vpc?ref=main"

  name                 = "dev"
  vpc_cidr             = "10.0.0.0/16"

  public_subnet_cidr   = "10.0.1.0/24"
  public_subnet_az = "us-east-1a"

  private_subnet_cidrs = ["10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_azs = ["us-east-1a", "us-east-1b"]
}


resource "aws_db_subnet_group" "dev_rds" {
  name       = "rds-subnet-group"
  subnet_ids = module.dev_vpc.private_subnet_ids

  tags = {
    Name = "dev-rds-subnet-group"
  }
}


resource "aws_security_group" "dev_rds" {
  name        = "dev-rds-sg"
  description = "Allow DB traffic"
  vpc_id      = module.dev_vpc.vpc_id

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.dev_vpc.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "dev-rds-sg"
  }
}
