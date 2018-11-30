import cerberus
import sys

products = {
    'book': {'stock': 10, 'price': 10},
    'microphone': {'stock': 20, 'price': 20},
    'laptop': {'stock': 2, 'price': 1000}
}

calculate_price_schema = {
    'product_name': {'type': 'string', 'allowed': ['book','microphone','laptop']},
    'number': {'type': 'integer', 'min': 0, 'max': 10000}
}


def calculate_price(product_name, number):
    """Calculate a price given a product name."""
    d = {'product_name': product_name, 'number': number}
    v = cerberus.Validator(calculate_price_schema)
    if v.validate(d):
        price = products[product_name]['price'] * number
        return price
    else:
        return v.errors


def test_calculate_price():
    """Test ordering products."""

    # Test laptop pricing - happy path
    assert calculate_price('laptop', 1) == 1000
    assert calculate_price('laptop', 2) == 2000
    assert calculate_price('laptop', 10) == 10000

    # Test laptop pricing - sad/bad path
    assert calculate_price('laptop', -10) == {'number': ['min value is 0']}

    assert calculate_price('laptop', 'asdf') == {'number': ['must be of integer type']}
    assert calculate_price('laptop', 0.0001) == {'number': ['must be of integer type']}

    assert calculate_price('laptop', sys.maxsize) == {'number': ['max value is 10000']}
    assert calculate_price('laptop', sys.maxsize**1000) == {'number': ['max value is 10000']}

    assert calculate_price('laptop', -sys.maxsize**1000) == {'number': ['min value is 0']}

    assert calculate_price('table', 1) == {'product_name': ['unallowed value table']}
    assert calculate_price(u'\u1F4A3', 1) == {'product_name': ['unallowed value \u1f4a3']}
