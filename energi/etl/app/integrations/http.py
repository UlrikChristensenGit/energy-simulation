from requests import Session
from requests.adapters import HTTPAdapter, Retry


class RetrySession:

    def __new__(cls) -> Session:
        session = Session()

        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )

        session.mount("https://", HTTPAdapter(max_retries=retries))

        return session
