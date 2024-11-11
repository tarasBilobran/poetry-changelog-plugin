import httpx


class GitHubAPIClient:
    def __init__(self) -> None:
        self.client = httpx.Client(
            http2=True,
            base_url="https://api.github.com",
            headers={"Accept": "application/vnd.github.v3+json"}
        )

    def get_releases(
        self,
        organization: str,
        repository: str
    ) -> dict:
        response = self.client.get(f"/repos/{organization}/{repository}/releases")
        response.raise_for_status()
        return response.json()
