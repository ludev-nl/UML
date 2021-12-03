from django.db.models import Q
from model.models import *


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

"""
def extract_data(result, paths, classifier):
    paths_copy = copy.deepcopy(paths)
    current_classifier = ""
    data = copy.deepcopy(result)
    while len(paths_copy[classifier]) > 1:
        current_classifier = paths_copy[classifier][0]
        paths_copy[classifier].remove(current_classifier)
        data = data[current_classifier]
        if len(data) > 1:
            returnable_data = []
            returnable_children = []
            next_classifier = paths_copy[classifier][0]
            for item in data['children']:
                info = extract_data(item[next_classifier], paths_copy, classifier)
                for data in info['data']:
                    returnable_data.append(data)
                for children in info['children']:
                    returnable_children.append(children)
            # print("========result=====")
            # print({classifier: {'data': returnable_data, 'children': returnable_children}})
            return {classifier: {'data': returnable_data, 'children': returnable_children}}
            # return returnable_data
        else:
            data = data[0]['children']
    # print(data)
    return data
"""