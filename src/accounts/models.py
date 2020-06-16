from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
	# user = models.OneToOneField(User)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	img = models.ImageField(upload_to="img", blank=True, null=True)
	# followers = models.ManyToManyField(User, related_name='followers')

class Follower(models.Model):
	user_from = models.ForeignKey(User, related_name='rel_from_set',on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return '{} sigue a {}'.format(self.user_from, self.user_to)

User.add_to_class('following',
	models.ManyToManyField('self',
		through=Follower,
		related_name='followers',
		symmetrical=False))
