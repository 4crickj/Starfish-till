"""
Class storing data for a single transaction.
"""

from decimal import Decimal

from till.tables import *
from till import config


class Product:
	"""Stores information about a single product in the sale."""
	
	def __init__(self, id, name, price, vat, qty=1, barcode=''):
		"""
		'price' and 'vat' should be decimal values to a maximum of two
		decimal places. 'price' is excluding VAT.
		"""
		self.id = id
		self.name = ''
		self.price = price
		self.vat = vat
		self.qty = qty
		self.barcode = barcode
	
	def total(self):
		"""
		Return the total cost to the buyer (price plus VAT all times the
		quantity).
		"""
		return (self.price + self.vat) * self.qty
	
	def total_vat(self):
		"""Return the total VAT."""
		return self.vat * self.qty


class Transaction:
	"""Stores information about a single transaction."""
	
	def __init__(self):
		self.id = '{0:0>3}-{1:0>6}'.format(config.get('tillid'), config.get('nextid'))
		config.set('nextid', int(config.get('nextid'))+1)
		self.products = []
		self.discount = Decimal('0.00')
	
	def add(self, product, qty=1):
		"""
		Add a product to the transaction. 'product' should be the storm
		model. 'qty' can be a positive or negative value and can be used
		to alter the quantity of an existing product (by adding 'qty' to
		the existing quantity).
		"""
		for p in self.products:
			if p.id == product.id:
				p.qty -= qty
				if p.qty <= 0:
					self.products.remove(p)
				return
		if qty <= 0:
			return
		self.products.append(Product(product.id, product.name, product.price, product.vat, qty, product.barcode))
	
	

