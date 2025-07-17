"""Base Service Initializer Module.

Description:
- This module contains ServiceInitializer class for direct usage in FastAPI
dependencies.

"""

from functools import _lru_cache_wrapper, lru_cache


class ServiceInitializer[T]:  # pylint: disable=too-few-public-methods
    """Service Initializer Class.

    :Description:
    - This class provides cached initialization for any service type.
    - Can be used directly in FastAPI Depends() without wrapper functions.

    """

    def __init__(self, service_class: type[T]) -> None:
        """Initialize with service class.

        :Args:
        - `service_class` (type[T]): The service class to initialize.
        **(Required)**

        """
        self._service_class: type[T] = service_class
        self._get_cached_service: _lru_cache_wrapper[T] = lru_cache(maxsize=1)(
            self._create_service
        )

    def _create_service(self) -> T:
        """Create service instance.

        :Description:
        - This method creates a new instance of the service class.

        :Args:
        - `None`

        :Returns:
        - `instance` (T): New instance of the service.

        """
        return self._service_class()

    def __call__(self) -> T:
        """Make the class callable for FastAPI dependency injection.

        :Description:
        - This method makes the ServiceInitializer instance callable, allowing
        it to be used directly with FastAPI's Depends().

        :Args:
        - `None`

        :Returns:
        - `instance` (T): Cached instance of the service.

        """
        return self._get_cached_service()
