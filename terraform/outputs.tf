output "alb_url" {
  value = aws_alb.application_load_balancer.dns_name
}

output "alb_dns_url" {
  value = aws_route53_record.alb_dns.name
}