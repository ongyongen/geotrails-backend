# Geotrails Backend
This is the backend for a Singapore based geocaching platform. Read more about it <a href="https://docs.google.com/presentation/d/1yEqSQ3rS5NhXwLe5_6I8wf7FZG98jVrbEIJTPvPHcYU/edit?usp=sharing">here</a> 

The aim of this platform is to:
- Help geocachers in Singapore plan for, manage and organize their geocaching trips
- Provide geocachers with access to advanced search and filtering criteria for geocaches in Singapore
- Provide geocachers with a comprehensive dashboard showcasing analytics of past geocaches found

# Tech Stack and Libraries Used
- Flask
- MongoDB

# Overall architecture
The backend of this platform is deployed to a Docker container and pushed to an Amazon ECR. 
From there, it is deployed to an Amazon EC2 instance with an Application Load Balancer using Amazon ECS. 
These resources are provisioned and managed using Terraform. <br></br>
<img width="573" alt="Screenshot 2023-09-16 at 12 14 28 PM" src="https://github.com/ongyongen/geotrails-frontend/assets/97529863/7d214699-910f-4040-886e-7442c2149829">

## Instructions to run the source code
Clone this repository to your local computer <br></br>
`git clone https://github.com/ongyongen/geotrails-backend.git`

Navigate to the root directory and set up a virtual environment <br></br>
`python -m venv env`

Activate the virtual environment <br></br>
`source env/bin/activate`

Install the required libraries <br></br>
`pip install -r requirements.txt`

#### Contents in the .env file
`MONGODB_URI=MONGODB_URI`

## Instructions to deploy scripts to AWS
Ensure that you have installed terraform : https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli <br></br>
Navigate to the `terraform` directory <br></br>
Run `terraform init` to set up the terraform config files. <br></br>
Run `terraform plan` to preview the changes that Terraform plans to make to your infrastructure. <br></br>
Run `terraform apply` to execute the actions propose in Terraform plan. <br></br>
Run `terraform destroy` to remove all resources previously configured by Terraform. <br></br>

Along the way you may be promopted to provide your AWS Access Key and AWS Secret Key. <br></br>
<img width="893" alt="Screenshot 2023-09-10 at 6 31 57 PM" src="https://github.com/ongyongen/govtech-gds-data-engineering-assessment/assets/97529863/725551d3-86b5-44fc-a64a-0bb16cc35615">

