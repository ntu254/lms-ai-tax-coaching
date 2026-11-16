"""Keep historical records while removing retired features from the LMS."""


def has_permission(doc, ptype="read", user=None):
	return False


def query_conditions(user=None):
	return "1=0"
