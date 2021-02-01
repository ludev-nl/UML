from django.shortcuts import render, get_object_or_404
from extractor.forms import UploadForm
from extractor.forms import SelectTitleForm
from extractor.tools.FileTools import *
from extractor.tools.extract import *
import threading
from model.models import *
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

store = sr.Recognizer()


def validator(uploadFile):
    if uploadFile.content_type not in ['audio/wav', 'text/plain']:
        return False
    else:
        return True


def get_large_audio_transcription(path):
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound,
                              min_silence_len=500,
                              silence_thresh=sound.dBFS - 14,
                              keep_silence=500,
                              )

    folder_name = 'audio-chunks'

    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ''

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f'chunk{i}.wav')
        audio_chunk.export(chunk_filename, format='wav')
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = store.record(source)
            try:
                text = store.recognize_google(audio_listened)
            except:
                print('Sorry...run again...')
            else:
                text = f'{text.capitalize()}. '
                print(chunk_filename, ': ', text)
                whole_text += text
    return whole_text


def upload_file(request):
    form = UploadForm()

    if request.method == 'POST':

        if 'convert' in request.POST:
            form = UploadForm(request.POST)
            if form.is_valid():
                file = Document(file=request.FILES['file'])
                file.save()
                if request.FILES['file'].content_type == 'audio/wav':
                    sound = AudioSegment.from_wav(file.file)
                    chunks = split_on_silence(sound,
                                              min_silence_len=500,
                                              silence_thresh=sound.dBFS - 14,
                                              keep_silence=500,
                                              )

                    folder_name = 'audio-chunks'

                    if not os.path.isdir(folder_name):
                        os.mkdir(folder_name)
                    whole_text = ''

                    for i, audio_chunk in enumerate(chunks, start=1):
                        chunk_filename = os.path.join(folder_name, f'chunk{i}.wav')
                        audio_chunk.export(chunk_filename, format='wav')
                        with sr.AudioFile(chunk_filename) as source:
                            audio_listened = store.record(source)
                            try:
                                text = store.recognize_google(audio_listened)
                            except:
                                print('Sorry...run again...')
                                return render(request, 'index.html', {'form': form, 'msg': 'Something wrong with conversion, please try again!'})
                            else:
                                text = f'{text.capitalize()}. '
                                print(chunk_filename, ': ', text)
                                whole_text += text
                    return render(request, 'index.html', {'form': form, 'text': whole_text})

                elif request.FILES['file'].content_type == 'text/plain':
                    file_path = file.file.path
                    print(file_path)
                    with open(file_path, 'r') as f:
                        text = f.read()
                        # print(text)
                        # print(type(text))
                    return render(request, 'index.html', {'form': form, 'text': text})

                else:
                    return render(request, 'index.html', {'form': form})

            else:
                msg = 'Please upload a txt file or an audio file.'

                return render(request, 'index.html', {'form': form, 'msg': msg})

        elif 'generate' in request.POST:
            txt = request.POST.get('text')
            print(txt)
            print(type(txt))
            title = request.POST.get('title')
            print(title)
            print(type(title))

            if title == '':
                msg = 'Please input a title'
                return render(request, 'index.html', {'form': form, 'msg': msg, 'text':txt})

            if txt == '':
                msg = 'Please input your requirement text'
                return render(request, 'index.html', {'form': form, 'msg': msg})

            else:
                path = 'data/' + title
                ftxt = path + '.txt'
                requirement = Requirement(title=title, raw_text=txt)
                requirement.save()
                save_text(ftxt, txt)
                uml = generate_uml(ftxt)
                return render(request, 'index.html', {'form': form, 'msg': 'Dispatched to CoreNLP Thread.', 'result': uml, 'text': txt})

    else:
        form = UploadForm()

    return render(request, 'index.html', {'form': form})


def select_title(request):
    title_form = SelectTitleForm()

    if request.method == 'POST':
        if 'DisplayText' in request.POST:

            title_form = SelectTitleForm(request.POST)

            if title_form.is_valid():
                req_id = title_form.cleaned_data['title']
                obj = get_object_or_404(Requirement, id=req_id)
                print(req_id)
                print(type(req_id))
                requirement = obj.raw_text
                print(requirement)
                print(type(requirement))
                return render(request, 'managreq.html', {'title_form': title_form, 'raw_text': requirement, 'id': req_id})

            else:
                msg = 'Please select a title.'

                return render(request, 'managreq.html', {'title_form': title_form, 'msg': msg})

        elif 'Update' in request.POST:

            req_id = request.POST.get('id')
            print(req_id)
            update_text = request.POST.get('raw_text')
            print(update_text)

            if update_text == '':
                msg = 'Please input requirement description.'
                return render(request, 'managreq.html', {'title_form': title_form, 'msg1': msg})
            else:
                Requirement.objects.filter(id=req_id).update(raw_text=update_text)
                msg = 'Update successfully!'
                return render(request, 'managreq.html', {'title_form': title_form, 'msg1': msg})

    else:
        title_form = SelectTitleForm()

    return render(request, 'managreq.html', {'title_form': title_form})



