from collections import defaultdict
import json

# create a defaultdict {entity:[label, alias, alias], entity:[label, alias]}
# from a csv file of labels formatted as "Q12345 \t 'Count von Count' \t en"
# TODO: language fallback
class LabelReader:

    def __init__(self, labels_file, lang=None, enable_fallback=True, unicode=False):
        self.fallback = []

        self.baseuri = "http://www.wikidata.org/entity/"

        self.d = defaultdict(list)
        self.fallback_d = defaultdict(list)

        if lang and enable_fallback:
            self.fallback_langs = self.getLangFallback(lang) 

        with open(labels_file) as f:
            for l in f:
                tmp = l.split("\t")
                if len(tmp) < 3:
                    continue
                # Unicode encoding
                if unicode:
                    tmp[1] = tmp[1].decode('unicode-escape')

                entity_id = tmp[0].strip().replace(self.baseuri, "")
                tmp_lang = tmp[2].replace('.','').strip()

                #if no language is set
                if lang == None:
                    self.d[entity_id].append(tmp[1].strip())
                    continue
                #if language is set
                if tmp_lang == lang:
                    self.d[entity_id].append(tmp[1].strip())
                # if language fallback is enabled
                elif enable_fallback and tmp_lang in self.fallback_langs:
                    if not entity_id in self.fallback_d:
                        self.fallback_d[entity_id] = {}
                    if not tmp_lang in self.fallback_d[entity_id]:
                        self.fallback_d[entity_id][tmp_lang] = [tmp[1].strip()]
                    else:
                        self.fallback_d[entity_id][tmp_lang].append(tmp[1].strip())

        # Needs proper testing and some more thought towards performance
        # if fallback is wanted, call the function to add lang fallbacks to the dict
        if enable_fallback:
            self.d = self.doLangFallback(self.d, self.fallback_d, self.fallback_langs)

    def get(self, uri):
        p = self.d[uri.strip().replace(self.baseuri, "")]
        return [i for i in p]

    # get the language fallback chain for a given language
    # language fallback as of Wikimedia language fallbacks
    def getLangFallback(self, lang):
        fallback = []
        # always fallback to English
        if not lang == 'en': 
            fallback.append('en')
        # load json file with all fallbacks
        with open('./datasets/fallbacks.json') as data_file:    
            fallbacks = json.load(data_file)
            if lang in fallbacks:
                fallback.extend(fallbacks[lang])
        return fallback

    def doLangFallback(self, d, fall, langs):
        # add fallbacks for missing values
        for k,v in fall.iteritems():
            if not k in d:
                for lang in langs:
                    if lang in fall[k]:
                        d[k] = fall[k][lang]
                        continue
        return d


        