from django.db import models


class Object(models.Model):
    n_predicts = models.IntegerField(default=7)
    n_splits = models.IntegerField(default=3)
    status = models.CharField(max_length=200)

    def __str__(self):
        return str(self.n_predicts)+" "+str(self.n_splits)+" "+self.status