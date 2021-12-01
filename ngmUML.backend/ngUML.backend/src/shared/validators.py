from django.core.exceptions import ValidationError


def rule_1(value):
	if int(value) > 50:
		return True
	else:
		raise ValidationError(
			'{value} does not abide by rule: '.format(value) + 'Product.price > 50',
			params={'value': value}, )
