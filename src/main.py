"""Application entry point – run the API server."""

import uvicorn

from src.config import settings


def main() -> None:
    """Start the uvicorn server."""
    uvicorn.run(
        "src.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
    )


if __name__ == "__main__":
    main()
