from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Test(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["title"]

	def __str__(self):
		return self.title

	def get_personality_for_score(self, score):
		return self.personalities.filter(min_score__lte=score, max_score__gte=score).order_by("min_score").first()


class Question(models.Model):
	test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
	text = models.CharField(max_length=500)
	order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.test.title} - Q{self.order}"


class Answer(models.Model):
	question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
	text = models.CharField(max_length=500)
	points = models.IntegerField(default=0)
	order = models.PositiveIntegerField(default=1)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self):
		return f"{self.question} - {self.points} punti"


class PersonalityProfile(models.Model):
	test = models.ForeignKey(Test, related_name="personalities", on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	min_score = models.IntegerField()
	max_score = models.IntegerField()

	class Meta:
		ordering = ["min_score", "id"]

	def __str__(self):
		return f"{self.test.title} - {self.name} ({self.min_score}-{self.max_score})"

	def clean(self):
		if self.min_score > self.max_score:
			raise ValidationError("Il punteggio minimo non può essere maggiore del massimo.")


class TestResult(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="test_results", on_delete=models.CASCADE)
	test = models.ForeignKey(Test, related_name="results", on_delete=models.CASCADE)
	score = models.IntegerField()
	personality = models.ForeignKey(
		PersonalityProfile,
		related_name="results",
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.user} - {self.test.title} ({self.score})"
