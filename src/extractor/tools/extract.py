from stanfordcorenlp import StanfordCoreNLP
import logging
from nltk.tokenize import sent_tokenize
from nltk.tree import Tree
from nltk import stem
import os
from model.generators.ClassifierGenerator import ClassifierGenerator
from model.generators.RelationshipGenerator import RelationshipGenerator
from model.generators.PropertyGenerator import PropertyGenerator
from model.models import Class, Classifier, Relationship, Property, Composition, Association



# word lists
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
              'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
              'themselves', 'what', 'who', 'whom', 'this', 'these', 'those', 'examples', 'but', 'because', 'until',
              'while', 'at', 'about', 'between', 'if', 'with', 'through', 'during', 'after', 'above', 'below', 'up',
              'down', 'able', 'form', 'of', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
              'where', 'why', 'how', 'all', 'both', 'each', 'few', 'most', 'other', 'some', 'no', 'nor', 'not', 'only',
              'own', 'same', 'than', 'too', 'very', 's', 't', 'just', 'don', "don't", 'should', 'now', 'd', 'll', 'm',
              'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', 'didn', 'doesn', "doesn't", 'hadn', 'hasn',
              'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', "wasn t", 'weren', 'weren t',
              'won', 'won t', 'wouldn', 'wouldn t', 'multiple', 'many', 'forward', 'etc', 'shall', 'also', 'therefore',
              'might', 'able', 'various', 'necessary', 'several', 'usually', 'must', 'finally', 'different', 'firstly',
              'corresponding', 'enough', 'relevant', '’s', 'furthermore', 'desired', 'typically', 'initially',
              'additional']

sto_words_further = ['their', 'such', 'as', 'them', 'will', 'that', 'when', 'they', 'for', 'may', 'types', 'specific',
                     'particular']


composition_word = ['have', 'has', 'contains', 'contain', 'contained', 'composed of', 'maintain', 'maintains',
                    'maintained', 'consists of', 'hold', 'holds', 'held', 'include', 'includes', 'included',
                    'divided to', 'has part', 'comprise', 'carry', 'involve', 'imply', 'embrace', 'is for', 'consist',
                    'consists']

# subtyping_word = ['is a', 'is a kind of', 'are', 'are classified as', 'can be', 'is classified as']

subtyping_word = ['is a', 'is a kind of', 'is', 'can be', 'are', 'can involve', 'be']

design_elements = ['system', 'user', 'application', 'data', 'computer', 'object', 'information', 'interface', 'online']

attribute_words = ['id', 'first name', 'last name', 'name', 'address', 'email', 'number','no', 'code', 'date', 'type',
                   'volume', 'birth', 'password', 'price', 'quantity', 'location', 'resolution date', 'creation date',
                   'crime code', 'course name', 'time slot', 'quantities', 'delivery date', 'prices',
                   'delivery address', 'scanner', 'till', 'illness conditions', 'diagnostic result', 'suggestions',
                   'birth date', 'order number', 'total cost', 'entry date', 'delivery status', 'description',
                   'product number']

# settings
class SubStanfordCoreNLP(StanfordCoreNLP):
    def __init__(self, path_or_host, port=None, memory='4g', lang='en', timeout=1500, quiet=True,
                 logging_level=logging.WARNING):
        super(SubStanfordCoreNLP, self).__init__(path_or_host, port, memory, lang, timeout, quiet, logging_level)

    def open_ie(self, sentence):
        r_dict = self._request('openie', sentence)
        openies = [(ie['subject'], ie['relation'], ie['object'])
                   for s in r_dict['sentences'] for ie in s['openie']]
        return openies


nlp = SubStanfordCoreNLP('http://corenlp', port=9000)

lemmatizer = stem.WordNetLemmatizer()


# check attribute and return in dic or lst
def check_attr(s):
    cls = {'Class': set(), 'Attribute': []}
    # check if object belongs to attribute and subject doesn't belong to attribute
    if s[0] in attribute_words and s[0] not in cls['Attribute']:
        cls['Attribute'].append(s[0])
        c = lemmatizer.lemmatize(s[2], pos='n').capitalize()
        cls['Class'] = c
        return cls

    # check if subject belongs to attribute and object belongs to class
    elif s[2] in attribute_words and s[2] not in cls['Attribute']:
        cls['Attribute'].append(s[2])
        c = lemmatizer.lemmatize(s[0], pos='n').capitalize()
        cls['Class'] = c
        return cls
    else:
        c1 = lemmatizer.lemmatize(s[0], pos='n').capitalize()
        c2 = lemmatizer.lemmatize(s[2], pos='n').capitalize()
        return [{'Class': c1, 'Attribute': []}, {'Class': c2, 'Attribute': []}]


# direction extract
def get_dir2(s):
    dir = {'from': set(), 'to': set()}
    raw_cls = [s[0], s[2]]
    raw_dir = []

    if s[0] in attribute_words or s[2] in attribute_words:
        raw_cls.clear()
        return None
    else:
        for words in raw_cls:
            words = words.split(' ')
            a = []
            for w in words:
                neww = lemmatizer.lemmatize(w, pos='n').capitalize()
                a.append(neww)
            b = ''.join(a)
            raw_dir.append(b)

        # using dependency parser to check and define direction between classes
        tri = list(s)
        joint_s = ' '.join(tri)
        dep = nlp.dependency_parse(joint_s)

        firstelement = []
        for d in dep:
            if d[0] not in firstelement:
                firstelement.append(d[0])

        if raw_dir[0] != raw_dir[1]:
            if 'nsubj' in firstelement:
                dir['from'] = raw_dir[0]
                dir['to'] = raw_dir[1]
            elif 'nsubjpass' in firstelement:
                dir['from'] = raw_dir[1]
                dir['to'] = raw_dir[0]
            else:
                dir['from'] = raw_dir[0]
                dir['to'] = raw_dir[1]

            return dir

        else:
            return None


# relationship extraction
def get_rels2(s):
    rel = {}
    # using dependecny parser to check active and passive voice
    tri = list(s)
    joint_s = ' '.join(tri)
    dep = nlp.dependency_parse(joint_s)

    firstelement = []
    for d in dep:
        if d[0] not in firstelement:
            firstelement.append(d[0])

    convertrel = []
    if 'nsubjpass' in firstelement:
        pos = nlp.pos_tag(s[1])
        for p in pos:
            if p[1] == 'VBN':
                convertrel.append(p[0])
        # using lemmatizer to transfer passive verb to active
        relname = lemmatizer.lemmatize(convertrel[0], pos='v')
        if relname in composition_word:
            rel['Composition'] = relname
        elif relname in subtyping_word:
            rel['Subtyping'] = ''
        else:
            rel['Association'] = relname

    else:
        if s[1] in composition_word:
            rel['Composition'] = s[1]
        elif s[1] in subtyping_word:
            rel['Subtyping'] = ''
        else:
            rel['Association'] = s[1]
    return rel


# multiplicity extraction
def get_multi():
    # set default multiplicity results as the widest range '0..*'
    multi = {'multiplicity': ['0..*', '0..*']}
    return multi


# subtyping multiplicity
def get_multi2():
    multi = {'multiplicity': ['', '']}
    return multi

# composition multiplicity
def get_multi3():
    multi = {'multiplicity': ['1', '0..*']}
    return multi

# check if object belongs to VBN
def obj_obj(s):
    new = []
    update =[]
    lst =[s[0], s[1]]
    obj = nlp.pos_tag(s[2])
    # print(obj)
    for i in obj:
        if i[1] != 'VBN':
            new.append(i[0])
    word = ' '.join(new)
    if word != '':
        lst.append(word)
        update = lst
    return update


# if openie fails
def get_triple(s):
    tri_lst = []
    try:
        np = s[0]
        vp = s[1]

        qnp = [np]
        while qnp:
            nps = qnp.pop(0)
            for ns in nps:
                if ns.label() == 'NP':
                    qnp.append(ns)
                elif ns.label() in ['NN', 'NNS', 'NNP']:
                    tri_lst.append(ns.leaves()[0])
        qvp = [vp]
        while qvp:
            vbs = qvp.pop(0)
            for vs in vbs:
                if vs.label() in ['VP', 'NP', 'PP']:
                    qvp.append(vs)
                elif vs.label() in ['VB', 'VBN', 'VBZ']:
                    tri_lst.append(vs.leaves()[0])
                elif vs.label() in ['NN', 'NNS', 'NNP']:
                    tri_lst.append(vs.leaves()[0])
    except:
        print(s)
    triple = tuple(tri_lst)
    return triple


# Read file
# lowercase, and concatenating paragraphs
def get_lines(file_path):
    with open(file_path, 'r') as f:
        raw_data = f.read().lower()
    lines = raw_data.split('\n')
    filtered_lines = [s for s in lines if s != '']
    initial_text = ' '.join(filtered_lines)
    print(initial_text)
    return initial_text


# text pre-processing
def preprocessing(fp):
    standard_txt = []

    initial_text = get_lines(fp)
    sents = sent_tokenize(initial_text)

    # preprocessing sentence by sentence
    for s in sents:
        tokens = nlp.word_tokenize(s)
        print(tokens)
        filtered_tokens = [token for token in tokens if token not in design_elements]
        line = ' '.join(filtered_tokens)

        # remove stopwords for openie
        word = nlp.word_tokenize(line)
        filtered_stop = [w for w in word if w not in stop_words]
        ie_sent = ' '.join(filtered_stop)
        print(ie_sent)

        ies = nlp.open_ie(ie_sent)
        print(ies)

        process_ies = []
        for item in ies:
            new_item = []
            for word in item:
                filtered_word = nlp.word_tokenize(word)
                update_word = [i for i in filtered_word if i not in sto_words_further]

                update_tri = ' '.join(update_word)
                new_item.append(update_tri)

            if '' not in new_item:
                #
                new = obj_obj(new_item)
                if len(new) != 0:
                    new1 = tuple(new)
                    process_ies.append(new1)

        print(process_ies)

        # if openie fails
        if len(ies) == 0:
            parser = nlp.parse(ie_sent)
            tree = Tree.fromstring(parser)
            root = tree[0]
            triple = get_triple(root)
            standard_txt.append(triple)
        else:
            for eachies in process_ies:
                if eachies not in standard_txt:
                    standard_txt.append(eachies)

    return standard_txt


# add
def generate_uml(fp):
    data = preprocessing(fp)
    objectDict = {}
    sum = []
    clsoutput = ''
    sumoutput = ''

    for s in data:
        check = check_attr(s)

        if isinstance(check, dict):
            raw_cls = [check['Class']]
            raw_dir = []
            for words in raw_cls:
                words = words.split(' ')
                a = []
                for w in words:
                    neww = lemmatizer.lemmatize(w, pos='n').capitalize()
                    a.append(neww)
                b = ''.join(a)
                raw_dir.append(b)
            # 不在，存入
            if raw_dir[0] not in objectDict:
                id = raw_dir[0]
                objectDict[id] = {}
                objectDict[id]['Class'] = raw_dir[0]
                objectDict[id]['Attribute'] = check['Attribute']
            # 在
            else:
                if raw_dir[0] not in objectDict[raw_dir[0]]['Attribute']:
                    # objectDict[check['Class']]['Attribute'].append(check['Atrribute'][0])
                    objectDict[raw_dir[0]]['Attribute'].extend(check['Attribute'])
        else:

            for item in check:
                raw_cls = [item['Class']]
                raw_dir = []
                for words in raw_cls:
                    words = words.split(' ')
                    a = []
                    for w in words:
                        neww = lemmatizer.lemmatize(w, pos='n').capitalize()
                        a.append(neww)
                    b = ''.join(a)
                    raw_dir.append(b)
                # print(raw_dir)
                # 不在
                if raw_dir[0] not in objectDict:
                    id = raw_dir[0]
                    objectDict[id] = {}
                    objectDict[id]['Class'] = raw_dir[0]
                    objectDict[id]['Attribute'] = []

        e = get_dir2(s)
        dir2 = e

        if dir2 != None:
            r = get_rels2(s)
            rels2 = r
            keys = list(rels2)
            if keys[0] == 'Subtyping':
                m = get_multi2()
                multi2 = m
            elif keys[0] == 'Composition':
                m = get_multi3()
                multi2 = m
            else:
                m = get_multi()
                multi2 = m
            sum.append(list(rels2.items()) + list(dir2.items()) + list(multi2.items()))

    # nlp.close()
    print(sum)
    print(objectDict)

    # format to display in textarea
    for item in objectDict.items():
        a = 'Class: ' + item[0] + '\n'
        a += '   Attribute: ' + str(item[1]['Attribute'])
        clsoutput += a + '\n'

    for s in sum:
        r = '\n' + '\n' + '{}: {}'.format(s[0][0], s[0][1])
        d1 = '\n' + '{}: {}'.format(s[1][0], s[1][1])
        m1 = '\n' + '  {}: {}'.format(s[3][0], s[3][1][0])
        d2 = '\n' + '{}: {}'.format(s[2][0], s[2][1])
        m2 = '\n' + '   {}: {}'.format(s[3][0], s[3][1][1])
        sumoutput += r + d1 + m1 + d2 + m2

    output = clsoutput + sumoutput

    print(output)

    # save into Ralph's demo
    for item in objectDict.items():
        classifier = Class(name=item[0])
        classifier.save()
        ClassifierGenerator(classifier).generate(False)
        # save attributes
        if item[1]['Attribute'] != '':
            get_cls = Classifier.objects.get(name=item[0])
            for i in item[1]['Attribute']:
                i = '_'.join(i.split(' '))
                attr = Property(name=i, classifier=get_cls)
                attr.save()
                PropertyGenerator(attr).generate(False)

    # save relation and direction into Ralph's demo
    for item in sum:
        # direction
        cls_from_name = item[1][1]
        cls_to_name = item[2][1]
        # get class name
        cls_from = Classifier.objects.get(name=cls_from_name)
        cls_to = Classifier.objects.get(name=cls_to_name)

        # passing an instance rather than a variable
        # relationship = Relationship(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from)
        # relationship.save()

        if item[0][0] == 'Composition':
            composition = Composition(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from,
                                      multiplicity_to=item[3][1][1], multiplicity_from=item[3][1][0],
                                      end_from=item[1][1], end_to=item[2][1])
            composition.save()
            RelationshipGenerator(composition).generate(False)
            # if Ralph's demo cannot execute many to many, replace the above code with this:
            # composition = Composition(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from,
            #                           multiplicity_to='0..*', multiplicity_from='1',
            #                           end_from=item[1][1], end_to=item[2][1])
            # composition.save()
            # RelationshipGenerator(composition).generate(False)

        elif item[0][0] == 'Association':
            association = Association(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from,
                                      multiplicity_to=item[3][1][1], multiplicity_from=item[3][1][0],
                                      end_from=item[1][1], end_to=item[2][1])
            association.save()
            RelationshipGenerator(association).generate(False)
            # if Ralph's demo cannot execute many to many, replace the above code with this:
            # association = Association(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from,
            #                           multiplicity_to='0..*', multiplicity_from='1',
            #                           end_from=item[1][1], end_to=item[2][1])
            # association.save()
            # RelationshipGenerator(association).generate(False)

        else:
            relationship = Relationship(name=item[0][1], classifier_to=cls_to, classifier_from=cls_from)
            relationship.save()

    os.system('start /b python manage.py make_and_run_migrations')

    return output

