from cleo.io.inputs.argument import Argument

from poetry.console.commands.command import Command

from poetry.plugins.application_plugin import ApplicationPlugin

from ._pypi_api_client import PyPIAPIClient
from ._github_api_client import GitHubAPIClient


class ShowChangelogCommand(Command):
    name = "show-changelog"
    description = "description tba."
    help = "tba."

    arguments = [Argument("package", required=True)]

    def __init__(self) -> None:
        super().__init__()
        self._github_api_client = GitHubAPIClient()
        self._pypi_api_client = PyPIAPIClient()

    def handle(self) -> int:
        if not self.poetry.locker.is_locked():
            self.line_error(
                "<error>Error: poetry.lock not found. Run `poetry lock` to create"
                " it.</error>"
            )
            return 1

        package_name = self.argument("package")

        locked_repo = self.poetry.locker.locked_repository()

        pkg = None
        for locked in locked_repo.packages:
            if locked.name == package_name:
                pkg = locked
                break

        print(pkg)
        print(self.poetry)
        print(package_name)

        # package = "poetry"
        self.info(f"Looking for a changelog for package '{package_name}'. "
                  f"Between versions 1.8.4 and 1.8.2")

        details = self._pypi_api_client.get_package_details(package_name)
        # Example 'https://github.com/python-poetry/poetry'
        github_url = details["info"]["project_urls"]["Repository"]
        *_, organization, repository = github_url.split("/")

        releases = self._github_api_client.get_releases(organization, repository)
        # For poc only grep first 5 rows
        rows = sorted(releases, key=lambda x: x["tag_name"], reverse=True)[:5]

        for row in rows:
            self.info(f"## RELEASE: {row['tag_name']}")
            self.info(row["body"])

        return 0


def factory():
    return ShowChangelogCommand()


class MultiProjectPlugin(ApplicationPlugin):

    def activate(self, application):
        application.command_loader.register_factory("show-changelog", factory)


__all__ = ["MultiProjectPlugin"]