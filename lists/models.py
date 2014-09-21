from django.db import models

class List(models.Model):
	def __str__(self):
		return '{List %d}'%(self.id)

class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)
	def __str__(self):
		return (' %s '%self.text)