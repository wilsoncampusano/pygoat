from django.db import models


class Item(models.Model):
	text = models.TextField(default='')
	
	def __str__(self):
		return (' %s '%self.text)