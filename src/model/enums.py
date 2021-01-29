import enum


class LinkType(enum.Enum):
    Association = "Association"
    DirectedAssociation = "DirectedAssociation"
    Aggregation = "Aggregation"
    Composition = "Composition"
    Inheritance = "Inheritance"
    Realization = "Realization"
    Dependency = "Dependency"

    @classmethod
    def choices(types):
        return tuple((i.name, i.value) for i in types)


class Type(enum.Enum):
    String = "string"
    Int = "int"
    Bool = "bool"

    @classmethod
    def choices(types):
        return tuple((i.name, i.value) for i in types)
