"""Base Service Initializer Module.

Description:
- This module contains ServiceInitializer class for direct usage in FastAPI
dependencies.

"""

from typing import ClassVar, Self, cast


class ServiceInitializer[T]:
    """Service Initializer Class.

    :Description:
    - This class implements singleton pattern for service initialization.
    - It can be used directly in FastAPI Depends() without wrapper functions.

    """

    _cache: ClassVar[dict[type, "ServiceInitializer[object]"]] = {}

    def __init__(self, service_class: type[T]) -> None:
        """Initialize ServiceInitializer instance.

        :Description:
        - This method initializes instance attributes.
        - Only called once per service class due to singleton pattern.

        :Args:
        - `service_class` (type[T]): Service class to initialize.
        **(Required)**

        :Returns:
        - `None`

        """
        self._service_class: type[T] = service_class
        self._service_instance: T | None = None

    def __new__(cls, service_class: type[T]) -> "ServiceInitializer[T]":
        """Create or return existing ServiceInitializer instance.

        :Description:
        - This method ensures only one ServiceInitializer instance per service
        class.

        :Args:
        - `service_class` (type[T]): Service class to initialize.
        **(Required)**

        :Returns:
        - `instance` (ServiceInitializer[T]): Cached or new ServiceInitializer
        instance.

        """
        if service_class not in cls._cache:
            instance: Self = super().__new__(cls)
            cls._cache[service_class] = instance

        return cast("ServiceInitializer[T]", cls._cache[service_class])

    def __call__(self) -> T:
        """Make class callable for FastAPI dependency injection.

        :Description:
        - This method returns cached service instance or creates one if it
        doesn't exist.

        :Args:
        - `None`

        :Returns:
        - `instance` (T): Cached instance of service.

        """
        if self._service_instance is None:
            self._service_instance = self._service_class()

        return self._service_instance
