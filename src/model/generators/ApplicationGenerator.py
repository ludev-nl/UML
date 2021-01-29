import os
from shutil import copyfile
from shutil import rmtree


def generate_urls(application):
    os.mkdir(application.name + '/views')
    copyfile('model/templates/files/template_urls.py', application.name + '/urls.py')
    copyfile('model/templates/files/template_views_init.py', application.name + '/views/__init__.py')

    f = open("thesis/urls.py", "r")
    contents = f.readlines()
    index = contents.index(']\n')
    f.close()
    value = '    path(\'' + application.name + '/\', include(\'' + application.name + '.urls\')),\n'
    contents.insert(index, value)

    f = open("thesis/urls.py", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

    f = open(application.name + "/urls.py", "r")
    contents = f.readlines()
    index = contents.index(']\n')
    f.close()
    value = '    path(\'\', views.index),\n'
    contents.insert(index, value)

    f = open(application.name + "/urls.py", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


def remove_urls(application):
    f = open("backend/urls.py", "r")
    contents = f.readlines()
    value = '    path(\'' + application.name + '/\', include(\'' + application.name + '.urls\')),\n'
    f.close()
    contents.remove(value)

    f = open("backend/urls.py", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


def generate_installed_app(application):
    f = open("backend/settings.py", "r")
    contents = f.readlines()
    index = contents.index('INSTALLED_APPS = [\n') + 1
    f.close()
    value = '    \'' + application.name + '.apps.' + application.name.capitalize() + 'Config\',\n'
    contents.insert(index, value)

    f = open("backend/settings.py", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


def remove_installed_app(application):
    f = open("backend/settings.py", "r")
    contents = f.readlines()
    value = '    \'' + application.name + '.apps.' + application.name.capitalize() + 'Config\',\n'
    f.close()
    contents.remove(value)

    f = open("backend/settings.py", "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


class ApplicationGenerator:
    def __init__(self, application):
        self.application = application

    def generate(self):
        os.system('python manage.py startapp ' + self.application.name)
        generate_urls(self.application)
        generate_installed_app(self.application)

    def delete(self):
        rmtree(self.application.name, ignore_errors=True)
        remove_urls(self.application)
        remove_installed_app(self.application)

