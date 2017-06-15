from collections import defaultdict

# create a defaultdict {entity:[label, alias, alias], entity:[label, alias]}
# from a csv file of labels formatted as "Q12345 \t 'Count von Count' \t en"
# TODO: language fallback
class LabelReader:

    def __init__(self, labels_file, lang=None):
        self.fallback = []

        self.baseuri = "http://www.wikidata.org/entity/"

        self.d = defaultdict(list)
        self.fallback_d = defaultdict(list)

        if lang:
            self.fallback = getLangFallback(lang)

        with open(labels_file) as f:
            for l in f:
                tmp = l.split("\t")
                entity_id = tmp[0].strip().replace(self.baseuri, "")

                #if no language is set
                if lang == None:
                    self.d[entity_id].append(tmp[1].strip())
                    continue

                #if language is set
                if tmp[2].strip() == lang:
                    self.d[entity_id].append(tmp[1].strip())
                #start building something for language fallback
                elif not self.d[entity_id] and tmp[2].strip() in self.fallback:
                    self.fallback_d[entity_id].append({tmp[2].strip(): tmp[1].strip()})
                    self.d[entity_id] = []

        # Needs proper testing and some more thought towards performance
        #doLangFallback(self.d, self.fallback_d, self.fallback)



    def get(self, uri):
        p = self.d[uri.strip().replace(self.baseuri, "")]
        return [i for i in p]

    def getLangFallback(lang):
        fallback = []
        return fallback.append('en')

    # TODO: Add actual list of fallbacks
    def doLangFallback(d, fall, langs):
        # add fallbacks for missing values
        for k,v in d:
            if not v:
                if v in fall:
                    for lang in langs:
                        if fall[k][lang]:
                            d[k] = fall[k][lang]
                            continue


        