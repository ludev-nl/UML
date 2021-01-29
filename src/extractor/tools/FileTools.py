from django.http import HttpResponse, Http404, FileResponse


def handle_upload_file(txt, file):
    try:
        with open(txt, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            return True
    except:
        return False


def save_text(file, text):
    with open(file, 'w') as f:
        f.write(text)


def write_uml(uml, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(uml)
