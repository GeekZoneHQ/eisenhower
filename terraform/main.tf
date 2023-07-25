terraform {
  cloud {
    organization = "geekzone"
    workspaces {
      name = "eisenhower"
    }
  }

  required_providers {
    dockerhub = {
      source  = "BarnabyShearer/dockerhub"
      version = "0.0.15"
    }
  }
}
