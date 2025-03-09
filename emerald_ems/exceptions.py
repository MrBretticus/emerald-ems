class EmeraldApiClientError(Exception):
	"""Exception to indicate a general API error."""
	
class EmeraldApiClientResponseError(EmeraldApiClientError):
	"""Exception to indicate an error in the response body"""

class EmeraldApiClientCommunicationError(EmeraldApiClientError):
	"""Exception to indicate a communication error."""

class EmeraldApiClientAuthenticationError(EmeraldApiClientError):
	"""Exception to indicate an authentication error."""

class EmeraldApiClientAuthorisationError(EmeraldApiClientError):
	"""Exception to indicate an authorisation error."""
