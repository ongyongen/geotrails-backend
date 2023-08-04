data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = [
        "sts:AssumeRole"
    ]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

data "aws_iam_policy" "AmazonEC2ContainerRegistryFullAccess" {
  arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
}

data "aws_acm_certificate" "certificate" {
  domain      = "geotrails.net"
  statuses    = ["ISSUED"]
  most_recent = true
}