from django.db import models
from .enums import Type


class Document(models.Model):
    file = models.FileField(upload_to='data/%Y-%m-%d')
    content = models.TextField()

    def __str__(self):
        return self.content


class Requirement(models.Model):
    title = models.CharField(max_length=255, unique=True)
    raw_text = models.TextField()
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.raw_text


class Classifier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_abstract = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=255, unique=True)
    classifiers = models.ManyToManyField(Classifier)


class Class(Classifier):
    pass


class Enumerator(Classifier):
    pass


class Property(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=Type.choices()
    )
    applications = models.ManyToManyField(Application)
    classifier = models.ForeignKey(
        Classifier,
        on_delete=models.CASCADE,
        related_name='classifier')

    def __str__(self):
        return self.name


class Operation(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=Type.choices())
    implementation = models.TextField(default='raise NotImplementedError')
    classifier = models.ForeignKey(
        Classifier,
        on_delete=models.CASCADE,
        related_name='operation_classifier')

    def __str__(self):
        return self.name


class OperationParameter(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=20,
        choices=Type.choices())
    operation = models.ForeignKey(
        Operation,
        on_delete=models.CASCADE,
        related_name='operation')

    def __str__(self):
        return self.name


class Relationship(models.Model):
    name = models.CharField(max_length=255, default='')
    classifier_to = models.ForeignKey(
        Classifier,
        on_delete=models.CASCADE,
        related_name='classifier_to')
    classifier_from = models.ForeignKey(
        Classifier,
        on_delete=models.CASCADE,
        related_name='classifier_from')

    def __str__(self):
        return self.name


class Association(Relationship):
    multiplicity_to = models.CharField(max_length=255)
    multiplicity_from = models.CharField(max_length=255)
    end_from = models.CharField(max_length=255, default='')
    end_to = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class DirectedRelationship(Relationship):
    class Meta:
        abstract = True


class Generalization(DirectedRelationship):
    pass
