class KaizenException(Exception):
    ...


class EntityAlreadyExists(KaizenException):
    ...


class EntityNotExists(KaizenException):
    ...


class PermissionDenied(KaizenException):
    ...
