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


def extract_data(result, paths, classifier):
    paths_copy = copy.deepcopy(paths)
    current_classifier = ""
    result_copy = copy.deepcopy(result)
    while len(paths_copy[classifier]) > 1:
        current_classifier = paths_copy[classifier][0]
        paths_copy[classifier].remove(current_classifier)
        result_copy = result_copy[current_classifier]
        if len(result_copy) > 1:
            returnable_data = []
            returnable_children = []
            next_classifier = paths_copy[classifier][0]
            for item in result_copy['children']:
                info = extract_data(item[next_classifier], paths_copy, classifier)
                for data in info['data']:
                    returnable_data.append(data)
                for children in info['children']:
                    returnable_children.append(children)
            print("========result=====")
            print({classifier: {'data': returnable_data, 'children': returnable_children}})
            return {classifier: {'data': returnable_data, 'children': returnable_children}}
            #return returnable_data
        else:
            data = data[0]['children']
    print(result)
    return result

def extract_data_from(source, target):
    return extract_data({"Product" : ["description"] }, get_pathing_from_classifier(source), target)


def make_children_list(data_paths):
    children = {}
    classifiers = [value for value in data_paths]
    for parent in data_paths:
        children[parent] = []
        classifiers.remove(parent)
        for classifier in classifiers:
            list = data_paths[classifier]
            if list[-2] == parent:
                children[parent].append(classifier)
    return children


def get_data(current_data, model, children, all_children):
    data = {'data': current_data, 'children': []}
    for i in range(len(current_data)):
        data_line = current_data[i]
        if len(children) > 0:
            data['children'].insert(i, {})
        for child in children:
            children_info = data['children'][i]
            lowercase = str(child).lower()
            if hasattr(data_line, lowercase):
                children_info[child] = get_data([getattr(data_line, lowercase)], child, all_children[child], all_children)
            else:
                query = {str(model).lower(): data_line.id}
                result = django_apps.get_model('shared', child).objects.filter(**query).all()
                children_info[child] = get_data(list(result), child, all_children[child], all_children)
    return data


def fill_data(page, queryset):
    data = {page.type: get_data(queryset, page.type, children[page.type], children)}


