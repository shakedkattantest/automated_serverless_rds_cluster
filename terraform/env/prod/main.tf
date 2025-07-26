locals {
  mysql_list    = ["mashu-db", "tov-db", "kore-db"]
  postgres_list = ["user-db", "payments-db", "analytics-db"]

  # Map DB name
  engine_map = merge(
    { for name in local.mysql_list    : name => { engine = "mysql" } },
    { for name in local.postgres_list : name => { engine = "postgres" } }
  )

  

  shared_settings = {
    instance_class       = "db.t3.micro"
    subnet_ids           = module.prod_vpc.private_subnet_ids
    security_group_ids   = ["sg-xxxxxxxxxxxx"]
    allocated_storage    = 20
    skip_final_snapshot  = true
  }

  rds_customs = {
    "payments-db" = {
      instance_class = "db.t3.small"
    },
    "analytics-db" = {
      allocated_storage = 100
    }
  }

  rds_list = concat(local.mysql_list, local.postgres_list)

  rds_definitions = {
    for name in local.rds_list :
    name => merge(
      local.shared_settings,
      local.engine_map[name],
      lookup(local.rds_customs, name, {}),
      { name = name }
    )
  }
}

module "rds_instances" {
  for_each = local.rds_definitions

  source               = "git::https://github.com/shakedkattan/automated_serverless_rds_cluster/tree/main/terraform/modules/rds?ref=main"

  name                 = each.value.name
  engine               = each.value.engine
  instance_class       = each.value.instance_class
  subnet_ids           = each.value.subnet_ids
  security_group_ids   = each.value.security_group_ids
  allocated_storage    = each.value.allocated_storage
  skip_final_snapshot  = each.value.skip_final_snapshot
}
