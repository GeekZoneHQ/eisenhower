resource "dockerhub_repository" "main" {
  name             = local.repo
  namespace        = local.org
  description      = "${local.repo} repository."
  full_description = "See http://GitHub.com/GeekZoneHQ/${local.repo}"
  private          = false
}
