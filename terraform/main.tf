# Create the ECR repo to store the backend API code
resource "aws_ecr_repository" "geotrails_backend_repo" {
  name = "geotrails_backend_repo"
}

# Create ECS Cluster
resource "aws_ecs_cluster" "geotrails_backend_cluster" {
  name = "geotrails_backend_cluster" 
}

# Create ECS Task Definition
resource "aws_ecs_task_definition" "geotrails_backend_task" {
  family                   = "geotrails_backend_task"
  container_definitions    = <<DEFINITION
  [
    {
      "name": "geotrails_backend_task",
      "image": "${aws_ecr_repository.geotrails_backend_repo.repository_url}",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
  DEFINITION
  requires_compatibilities = ["FARGATE"] 
  network_mode             = "awsvpc"    
  memory                   = 512         
  cpu                      = 256        
  execution_role_arn       = "${aws_iam_role.ecsTaskExecutionRole.arn}"
}

# Create an IAM role that allows ecs task execution 
resource "aws_iam_role" "ecsTaskExecutionRole" {
  name               = "ecsTaskExecutionRole"
  assume_role_policy = "${data.aws_iam_policy_document.assume_role_policy.json}"
}

# Give ecsTaskExecutionRole IAM policy of AmazonEC2ContainerRegistryFullAccess
resource "aws_iam_role_policy_attachment" "sto-readonly-role-policy-attach" {
  role       = "${aws_iam_role.ecsTaskExecutionRole.name}"
  policy_arn = "${data.aws_iam_policy.AmazonEC2ContainerRegistryFullAccess.arn}"
}

# Provide a reference to default VPC
resource "aws_default_vpc" "default_vpc" {
}

# Provide references to default subnets
resource "aws_default_subnet" "default_subnet_a" {
  availability_zone = "ap-southeast-1a"
}

resource "aws_default_subnet" "default_subnet_b" {
  availability_zone = "ap-southeast-1b"
}

# Create a security group for the load balancer
resource "aws_security_group" "load_balancer_security_group" {
  vpc_id      = aws_default_vpc.default_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] 
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ALB
resource "aws_alb" "application_load_balancer" {
  name               = "load-balancer-dev"
  load_balancer_type = "application"
  subnets = [ 
    "${aws_default_subnet.default_subnet_a.id}",
    "${aws_default_subnet.default_subnet_b.id}"
  ]
  security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
}

# Create load balancer target group
resource "aws_lb_target_group" "target_group" {
  name        = "target-group"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = "${aws_default_vpc.default_vpc.id}"
}

# Create load balancer listener for http
resource "aws_lb_listener" "http" {
  load_balancer_arn = "${aws_alb.application_load_balancer.arn}"
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "redirect" 

    redirect {
      port = "443"
      protocol = "HTTPS"
      status_code = "HTTP_301"
    }
    target_group_arn = "${aws_lb_target_group.target_group.arn}" 
  }
}

# Create load balancer listener for https
resource "aws_lb_listener" "https" {
  load_balancer_arn = "${aws_alb.application_load_balancer.arn}"
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
  certificate_arn   = data.aws_acm_certificate.certificate.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.target_group.arn
  }
}

# Associate load balancer with an SSL cert 
resource "aws_lb_listener_certificate" "ssl_certificate" {
  listener_arn    = aws_lb_listener.https.arn
  certificate_arn = data.aws_acm_certificate.certificate.arn
}

# Create an ECS service
resource "aws_ecs_service" "geotrails_backend_service" {
  name            = "geotrails_backend_service"  
  cluster         = "${aws_ecs_cluster.geotrails_backend_cluster.id}"  
  task_definition = "${aws_ecs_task_definition.geotrails_backend_task.arn}" 
  launch_type     = "FARGATE"
  desired_count   = 3 

  load_balancer {
    target_group_arn = "${aws_lb_target_group.target_group.arn}" 
    container_name   = "${aws_ecs_task_definition.geotrails_backend_task.family}"
    container_port   = 8000 
  }

  network_configuration {
    subnets          = ["${aws_default_subnet.default_subnet_a.id}", "${aws_default_subnet.default_subnet_b.id}"]
    assign_public_ip = true
    security_groups  = ["${aws_security_group.service_security_group.id}"]
  }
}

# Create an ECS security group
resource "aws_security_group" "service_security_group" {
  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    security_groups = ["${aws_security_group.load_balancer_security_group.id}"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_route53_record" "alb_dns" {
  zone_id = var.ROUTE53_ZONE_ID
  name    = "www.geotrails.net" 
  type    = "A"
  alias {
    name                   = aws_alb.application_load_balancer.dns_name
    zone_id                = aws_alb.application_load_balancer.zone_id  
    evaluate_target_health = true
  }
}
