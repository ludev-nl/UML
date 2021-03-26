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


class Composition(Relationship):
    multiplicity_to = models.CharField(max_length=255)
    multiplicity_from = models.CharField(max_length=255)
    end_from = models.CharField(max_length=255, default='')
    end_to = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


#################################################
#               Activity Model                  #
#################################################

# TODO
# - implement ValueSpecification
# - implement Behavior 
# - implement Operation

class Activity(models.Model):
    name = models.CharField(max_length=255, unique=False)
    precondition = models.CharField(max_length=255, unique=False)
    postcondition = models.CharField(max_length=255, unique=False)
    isReadOnly = models.BooleanField(default=False)
    isSingleExecution = models.BooleanField(default=False)

class ActivityNode(models.Model):
    name = models.CharField(max_length=255, unique=False)
    description = models.CharField(max_length=255, unique=False)
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='activitynode_activity'
    )
    # target_edge = models.ForeignKey(
    #     ActivityEdge,
    #     on_delete=models.CASCADE,
    #     related_name='target_edge'
    # )
    # source_edge = models.ForeignKey(
    #     ActivityEdge,
    #     on_delete=models.CASCADE,
    #     related_name='source_edge'
    # )

class ActivityEdge(models.Model):
    # Implement value specification
    # should be of type ValueSpecification
    guard = models.CharField(max_length=255, unique=False)
    weight = models.CharField(max_length=255, unique=False)

    # In the class diagram there are multiple incoming and outgoing activities
    incoming_node = models.ForeignKey(
        ActivityNode,
        on_delete=models.CASCADE,
        related_name='incoming_node'
    )
    outgoing_node = models.ForeignKey(
        ActivityNode,
        on_delete=models.CASCADE,
        related_name='outgoing_node'
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name='activityedge_activity'
    )

class ControlNode(ActivityNode):
    #Not instantiable
    pass

class InitialNode(ControlNode):
    def parentId(self):
        return self.controlnode_ptr_id

class FinalNode(ControlNode):
    #Not instantiable
    pass

class FlowFinalNode(FinalNode):
    def parentId(self):
        return self.finalnode_ptr_id
        #return self.FinalNode.id

class ActivityFinalNode(FinalNode):
    def parentId(self):
        return self.finalnode_ptr_id

class ForkNode(ControlNode):
    def parentId(self):
        return self.controlnode_ptr_id

class MergeNode(ControlNode):
    def parentId(self):
        return self.controlnode_ptr_id

class JoinNode(ControlNode):
    joinSpec = models.CharField(max_length=255, unique=False)
    isCombineDuplicate = models.BooleanField(default=True)
    def parentId(self):
        return self.controlnode_ptr_id

class DecisionNode(ControlNode):
    # Should be Behavior needs to be implemented
    decisionInput = models.CharField(max_length=255, unique=False)
    # Should be objectFlow needs to be implemented
    decisionInputFlow = models.CharField(max_length=255,unique=False)
    def parentId(self):
        return self.controlnode_ptr_id

class ExecutableNode(ActivityNode):
    pass

class Action(ExecutableNode):
    localPrecondition = models.CharField(max_length=255, unique=False)
    localPostcondition = models.CharField(max_length=255, unique=False)
    body = models.CharField(max_length=255, unique=False)
    #Todo Operation
    def parentId(self):
        return self.executablenode_ptr_id

