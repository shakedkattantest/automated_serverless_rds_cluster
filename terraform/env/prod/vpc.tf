module "prod_vpc" {
  source = "git::https://github.com/shakedkattan/automated_serverless_rds_cluster.git///terraform/modules/vpc?ref=main"

  name                 = "prod"
  vpc_cidr             = "10.0.0.0/16"

  public_subnet_cidr   = "10.0.1.0/24"
  public_subnet_az     = "eu-central-1a"

  private_subnet_cidrs  = ["10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_azs    = ["eu-central-1a", "eu-central-1b"]
}

resource "aws_db_subnet_group" "rds" {
  name       = "rds-subnet-group"
  subnet_ids = module.prod_vpc.private_subnet_ids

  tags = {
    Name = "${module.prod_vpc.name}-rds-subnet-group"
    Environment = module.prod_vpc.name
  }
}
