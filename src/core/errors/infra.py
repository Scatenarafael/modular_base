class InfraError(Exception):
    """Erros vindos de infraestrutura (DB, redes, filas, etc.)."""


class DatabaseError(InfraError): ...


class UniqueViolation(DatabaseError): ...


class ForeignKeyViolation(DatabaseError): ...


class DatabaseConnectionError(DatabaseError): ...


class ExternalServiceError(InfraError): ...


class ExternalServiceTimeout(ExternalServiceError): ...
