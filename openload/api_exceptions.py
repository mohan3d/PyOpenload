class BadRequestException(Exception):
    pass


class PermissionDeniedException(Exception):
    pass


class FileNotFoundException(Exception):
    pass


class TooManyRequestsException(Exception):
    pass


class UnavailableForLegalReasonsException(Exception):
    pass


class BandwidthUsageExceeded(Exception):
    pass


class ServerErrorException(Exception):
    pass
