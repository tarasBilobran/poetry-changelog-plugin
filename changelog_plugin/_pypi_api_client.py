import httpx


class PyPIAPIClient:
    def __init__(self) -> None:
        self.client = httpx.Client(base_url="https://pypi.org")

    def get_package_details(
        self,
        pkg_name: str
    ) -> dict:
        response = self.client.get(f"/pypi/{pkg_name}/json").json()
        response.raise_for_status()
        return response.json()
