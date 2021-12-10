from django.db.models import Q
from model.models import *
import copy


def loop_through_relationships(relationships, paths, added, new_paths, currentpath, start):
    # Loop through related classifiers in foreign keys
    for relationship in [rela for rela in relationships if (rela.multiplicity_to == '1' or rela.multiplicity_from == '1') and ((
                     rela.classifier_to not in paths or (
                         rela.classifier_to in paths and len(paths[rela.classifier_to]) > len(currentpath) + 1)) or (
                     rela.classifier_from not in paths or (
                        rela.classifier_from in paths and len(paths[rela.classifier_from]) > len(currentpath) + 1)))]:
        if relationship.classifier_to == start:
            new_currentpath = currentpath + [relationship.classifier_from] if len(currentpath) > 0 else [
                relationship.classifier_to, relationship.classifier_from]
            paths[relationship.classifier_from] = new_currentpath
            added.append(relationship.classifier_from)
        else:
            new_currentpath = currentpath + [relationship.classifier_to] if len(currentpath) > 0 else [
                relationship.classifier_from, relationship.classifier_to]
            paths[relationship.classifier_to] = new_currentpath
            added.append(relationship.classifier_to)
        new_paths.append(new_currentpath)


def get_possible_classifiers(start, paths, currentpath):
    added = []
    new_paths = []
    relationships = Association.objects.filter(Q(classifier_from=start) | Q(classifier_to=start)).all()
    loop_through_relationships(relationships, paths, added, new_paths, currentpath, start)
    relationships = Composition.objects.filter(Q(classifier_from=start) | Q(classifier_to=start)).all()
    loop_through_relationships(relationships, paths, added, new_paths, currentpath, start)

    for i, classifier in enumerate(added):
        get_possible_classifiers(classifier, paths, new_paths[i])
    return paths


def get_pathing_from_classifier(classifier):
    return get_possible_classifiers(classifier, {classifier: [classifier] }, [])



