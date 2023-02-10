class ProposalsException(Exception):
    ...


class EntityAlreadyExists(ProposalsException):
    ...


class EntityNotExists(ProposalsException):
    ...


class PermissionDenied(ProposalsException):
    ...
