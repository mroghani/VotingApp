from django.db import models


class Voter(models.Model):
    def __str__(self):
        return self.email
    email = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

class Candidate(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

