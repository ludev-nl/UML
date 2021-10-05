from django.shortcuts import render
from django.shortcuts import redirect
import string
from django.http import HttpResponse
from django.db.models import Q
from ..models import *
import json
from django.forms.models import model_to_dict
import os
from ..generators import *
import re
from django.apps import apps as django_apps

def add_category(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'GET':
        context = {
            'application': application,
        }
        return render(request, 'add_category.html', context)
    else:
        name = request.POST['name']
        category = Category(name=name.lower())
        category.save()
        application.categories.add(category)
        return redirect('/model/applications/' + application_id)


def add_page(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    if request.method == 'GET':
        context = {
            'application': application,
            'category': category
        }
        return render(request, 'add_page.html', context)
    else:
        name = request.POST['name']
        page = Page(name=name.lower())
        page.save()
        page.category.add(category)
        return redirect('/model/applications/' + application_id + '/category/' + category_id)


def show_category(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    pages = category.page_set.all()
    context = {
        'application': application,
        'category': category,
        'pages': pages,
    }
    return render(request, 'show_category.html', context)


def edit_category(request, application_id, category_id):
    return redirect('/model/applications/' + application_id)


def delete_category(request, application_id, category_id):
    application = Application.objects.get(id=application_id)
    category = application.categories.filter(id=category_id).get()
    category.delete()
    application.categories.remove(category)
    return redirect('/model/applications/' + application_id)


def loop_through_relationships(relationships, paths, added, new_paths, currentpath, model):
    for relationship in [rela for rela in relationships if (rela.multiplicity_to == '1' or rela.multiplicity_from == '1') and ((
                     rela.classifier_to.name not in paths or (
                         rela.classifier_to.name in paths and len(paths[rela.classifier_to.name]) > len(currentpath) + 1)) or (
                     rela.classifier_from.name not in paths or (
                        rela.classifier_from.name in paths and len(paths[rela.classifier_from.name]) > len(currentpath) + 1)))]:
        if relationship.classifier_to.name == model.name:
            new_currentpath = currentpath + [relationship.classifier_from.name] if len(currentpath) > 0 else [
                relationship.classifier_to.name, relationship.classifier_from.name]
            paths[relationship.classifier_from.name] = new_currentpath
            added.append(relationship.classifier_from)
        else:
            new_currentpath = currentpath + [relationship.classifier_to.name] if len(currentpath) > 0 else [
                relationship.classifier_from.name, relationship.classifier_to.name]
            paths[relationship.classifier_to.name] = new_currentpath
            added.append(relationship.classifier_to)
        new_paths.append(new_currentpath)


def get_possible_classifiers(page, model, paths, currentpath):
    added = []
    new_paths = []
    relationships = Association.objects.filter(Q(classifier_from=model) | Q(classifier_to=model)).all()
    loop_through_relationships(relationships, paths, added, new_paths, currentpath, model)
    relationships = Composition.objects.filter(Q(classifier_from=model) | Q(classifier_to=model)).all()
    loop_through_relationships(relationships, paths, added, new_paths, currentpath, model)

    for i, classifier in enumerate(added):
        get_possible_classifiers(page, classifier, paths, new_paths[i])
    return paths


def page_link_properties(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    classifiers = application.classifiers.all()
    page = Page.objects.get(id=page_id)
    allProperties = application.property_set
    selectedProperties = page.property_set.all()
    if page.data_paths == "":
        context = {
            'application': application,
            'page': page,
            'classifiers': classifiers,
            'msg': "You have to select a main model first"
        }
        return render(request, 'page_link_properties.html', context)
    else:
        paths = json.loads(page.data_paths)
    if request.method == "GET":
        for classifier in classifiers:
            if classifier.name not in paths:
                continue
            classifier.properties = []
            thisProperties = allProperties.filter(classifier=classifier.id).all()
            for property in [x for x in thisProperties]:
                if property in selectedProperties:
                    property.linked = True
                classifier.properties.append(property)
        context = {
            'application': application,
            'page': page,
            'classifiers': classifiers,
        }
        return render(request, 'page_link_properties.html', context)
    else:
        for property in allProperties.all():
            if property.classifier.name + "-" + property.name in request.POST:
                if page not in property.applications.all():
                    property.applications.add(page)
                    if property.classifier not in page.classifiers.all():
                        page.classifiers.add(property.classifier)
            else:
                if property.applications.filter(id=page_id).exists():
                    property.applications.remove(page)
                    if property.classifier in page.classifiers.all() and \
                            page.property_set.filter(~Q(id=property.id), classifier=property.classifier).count() == 0:
                        page.classifiers.remove(property.classifier)

        return redirect('/model/applications/' + application_id + '/page/' + page_id + '/properties')


def make_children_list(data_paths):
    print("==============")
    print(data_paths)
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
    data_paths = json.loads(page.data_paths)
    children = make_children_list(data_paths)
    data = {page.type: get_data(queryset, page.type, children[page.type], children)}
    return data, children


def show_page(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    page = Page.objects.get(id=page_id)
    all_sections = Section.objects.filter(linked_page=page).order_by("sorting").all()
    sections = change_sections(all_sections, False)

    page.query.replace('[id]', request.GET.get('id', ''))
    query = {}
    for value in page.query.split(","):
        split = value.split("=")
        query[split[0].strip()] = split[1].strip()
    queryset = django_apps.get_model('shared', page.type).objects.filter(**query).all()
    data, children = fill_data(page, queryset)

    html = make_html(sections, page, data, children, json.loads(page.data_paths))

    context = {
        'application': application,
        'page': page,
        'html': html,
    }
    return render(request, 'page_view.html', context)


def change_sections(all_sections, tojson):
    sections = {}
    for section in all_sections:
        section.children = {}
        sorting = section.sorting.split('.')
        target = sections
        if '.' in section.sorting:
            for sort in sorting[:-1]:
                target = target[int(sort)].children
        target[int(sorting[-1])] = section

    if tojson:
        sections = convert_section_to_json(sections)

    return sections


def convert_section_to_json(object):
    value = "["
    for item in object.values():
        value +='{"classes":"'+item.classes+'","content":"'+item.content.replace('"', '\\\"')+'","children":'+convert_section_to_json(item.children)+ '},'
    value = value if value[-1] == '[' else value[:-1]
    value += "]"
    return value


def extract_data(result, paths, classifier):
    paths_copy = paths #prevents deletion from main type
    current_classifier = ""
    data = result
    # print(result)
    while len(paths_copy[classifier]) > 1:
        current_classifier = paths_copy[classifier][0]
        paths_copy[classifier].remove(current_classifier)
        data = data[current_classifier]
        if len(data) > 1:
            returnable_data = []
            for item in data:
                returnable_data.append(extract_data(item['children'], paths_copy, classifier))
            return returnable_data
        else:
            data = data[0]['children']
    # print(data)
    return data[classifier]


def make_html(sections, page, result, children, paths):
    if sections == {}:
        return ''
    value = "<div class='row'>"
    # multiple line items per order
    for section in sections.values():
        has_information = "{{" in section.content
        maximum = 1
        section_data = {}
        for classifier in section.classifiers.all():
            lines = extract_data(result, paths, classifier.name)
            print("=========[lines]=======")
            print(lines)
            section_data[classifier.name] = [line for line in lines['data']]
            # section_data[classifier.name] = [line['data'] for line in extract_data(result, paths, classifier.name)]
            maximum = max(maximum, len(section_data[classifier.name]))
            print(section_data)
            print(classifier.name)
        print(section_data)
        for amount in range(0, maximum):
            children = make_html(section.children, page, result, children, paths)
            value += "<div class ='"+section.classes+"'>" \
                        "<div class='content'>"+section.content+"</div>" \
                        "<div class='children'>"+children+"</div></div>"
    value += "</div>"
    return value


# def fill_content(content, result):



def edit_page(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    page = Page.objects.get(id=page_id)
    allClassifiers = application.classifiers.all()
    classifiers = []
    properties = page.property_set
    all_sections = Section.objects.filter(linked_page=page).order_by("sorting").all()
    sections = change_sections(all_sections, True).replace('\n', '')
    for classifier in allClassifiers:
        classifier.properties = []
        classifier.machine_name = classifier.name.translate({ord(c): None for c in string.whitespace})
        classifierProperties = properties.filter(classifier=classifier).all()
        for property in classifierProperties:
            property.machine_name = property.name.translate({ord(c): None for c in string.whitespace})
            classifier.properties.append(property)
        if len(classifier.properties) > 0:
            classifiers.append(classifier)
    context = {
        'application': application,
        'page': page,
        'classifiers': classifiers,
        'sections': sections
    }
    return render(request, 'page_edit.html', context)


def save_page(request, application_id, page_id):
    page = Page.objects.get(id=page_id)
    Section.objects.filter(linked_page=page).delete()
    sections = json.loads(request.POST['sections'])
    make_sections(sections, page)
    return HttpResponse('')


def page_query(request, application_id, page_id):
    application = Application.objects.get(id=application_id)
    page = Page.objects.get(id=page_id)
    classifiers = application.classifiers.all()
    if request.method == "POST":
        page.type = request.POST['model']
        page.query = request.POST['filter']
        main = Classifier.objects.get(name=page.type)
        paths = {main.name: [main.name]}
        get_possible_classifiers(page, main, paths, [])
        page.data_paths = json.dumps(paths)
        page.save()
    context = {
        'application': application,
        'page': page,
        'classifiers': classifiers,
    }
    return render(request, 'page_query.html', context)


def make_sections(sections, page):
    for section in sections:
        new_section = Section.objects.create(
            name='page-'+str(page.id)+'section'+str(section['sorting']),
            classes=section['classes'],
            content=section['content'],
            sorting=section['sorting'],
            linked_page=page,
        )
        regex = r"{{(.+)-(.+)}}"
        touples = re.findall(r"{{([a-zA-Z]+)-([a-zA-Z_]+)}}", section['content'])
        for touple in touples:
            classifier = Classifier.objects.filter(name=touple[0]).get()
            new_section.classifiers.add(classifier)
        make_sections(section['children'], page)



def delete_page(request, application_id, page_id):
    page = Page.objects.get(id=page_id)
    category = page.category.get()
    page.delete()
    category.page_set.remove(page)
    return redirect('/model/applications/' + application_id)

