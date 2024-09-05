class ResourceNotFoundError(Exception):
    def __init__(self, resource: str):
        self.resource = resource

    def __str__(self):
        return "Resource not found: %s" % self.resource


class InvalidResourceError(Exception):
    def __init__(self, resource: str, reason: str | None = None):
        self.resource = resource
        self.reason = reason

    def __str__(self):
        if self.reason:
            return "Invalid resource: %s\nReason: %s" % (self.resource, self.reason)
        return "Invalid resource %s" % self.resource


class UnknownResourceError(Exception):
    def __init__(self, resource: str):
        self.resource = resource

    def __str__(self):
        return "Unknown resource: %s\nNo connector found for this resource." % self.resource
