provider "aws" {
  region = "us-east-2"
}

resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "cargoexpress2024"
  acl    = "public-read"

  website {
    index_document = "index.html"
  }
}

resource "aws_dynamodb_table" "pedidos" {
  name           = "PedidosEntregados"
  hash_key       = "IdRepartidor"

  attribute {
    name = "IdRepartidor"
    type = "S"
  }

  billing_mode = "PAY_PER_REQUEST"
}

resource "aws_lambda_function" "auth_login" {
  function_name = "auth-login-function"
  role          = aws_iam_role.lambda_exec.arn
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  source_code_hash = filebase64sha256("auth.zip")

  environment {
    variables = {
      JWT_SECRET = "mi-clave-secreta"
    }
  }
}

resource "aws_api_gateway_rest_api" "api" {
  name        = "CargoExpressAPI"
  description = "API for Cargo Express backend"
}

resource "aws_api_gateway_resource" "auth_login_resource" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "login"
}

resource "aws_api_gateway_method" "auth_login_method" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.auth_login_resource.id
  http_method   = "POST"
  authorization = "NONE"
}
