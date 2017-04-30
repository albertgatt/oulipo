'''
Created on 21 Sep 2015

@author: albertgatt
'''
from random import choice, random
import re
from Lexicon import verbs, wordlists
from string import Template
from base import BaseClasses as bc
from nltk.corpus import wordnet as wn

class RandomExpChooser(object):
    def __init__(self):
        pass
    
    def reshuffle(self,x):
        i = int(len(x)/2 + random() * (len(x) - len(x)/2))
        return [x[i]] + x[:i] + x[i+1:]
    

class TimeHelper(RandomExpChooser):
    
    def __init__(self):
        pass
    
    def time_expression(self, time):
        month = time.month
        hr = time.hour
        adjective = None
        monthname = wordlists.months[month - 1]
    
        if month in range(1, 4) or month == 12:
            adjective = self.reshuffle(wordlists.winter)[0]
        elif month in range(4, 6):
            adjective = self.reshuffle(wordlists.spring)[0]
        elif month in range(6, 9):
            adjective = self.reshuffle(wordlists.summer)[0]
        else:
            adjective = self.reshuffle(wordlists.autumn)[0]
        
        try:
            period_index = list(filter(lambda x: hr >= wordlists.times[x] and hr < wordlists.times[x + 1], range(0, len(wordlists.times) - 2)))[0]
            period = wordlists.periods[period_index].substitute(ADJ=adjective)
            time_string = wordlists.time1.substitute(PERIOD=period, MONTH=monthname)
            return time_string
        except:
            return None

    def event_conjunction(self):
        return choice(wordlists.temporal_conjunctions)
    
    def flashback_conjunction(self):
        return choice(wordlists.flashback_conjunctions)
    
    def switchback_conjunction(self):
        return choice(wordlists.switchback_conjunctions)
    
    def flashforward_conjunction(self):
        return choice(wordlists.flashforward_conjunctions)

class ArticleHelper(object): 
    
    def __init__(self):
        pass
    
    def indefinite_article(self, string):
        if re.match('^[aeiou]', string.strip()):
            return 'an'
        else:
            return 'a'
        
class OrthographyHelper(object):
    def __init__(self):
        pass
    
    def sentence_cap(self, line):
        return line[0].upper() + line[1:]
        #return ' '.join(s[0].upper() + s[1:] for s in line.split(' '))

class VerbConjugator(object):
    def __init__(self):
        pass
    
    def _run(self, function, verb):
        v = verb.split(' ')
        res = function(v[0])
        return ' '.join([res] + v[1:])
    
    def past_tense(self, verb):
        return self._run(verbs.verb_past, verb)
    
    def present_participle(self, verb):
        return self._run(verbs.verb_present_participle, verb)
    
    def past_participle(self, verb):
        return self._run(verbs.verb_past_participle, verb)
    
class ExpressionChooser(object):
    def __init__(self):
        self._syonyms = dict()
        self.ages = {19: 'teens', 29: 'twenties', 39:'thirties', 49:'forties', 59:'fifties', 69:'sixties', 79:'seventies'}
    
    def get_weapon(self):
        return choice(wordlists.weapons)
    
    def get_media_expression(self):
        return choice(wordlists.media)
    
    def _load_wn_adj_synonyms(self, syn, dep=3):
        try:
            sim = lambda s: s.similar_tos()
            synset = wn.synset(syn)
            lemmas = []
            
            for s in list(synset.closure(sim, depth=dep)):
                lemmas += [lemma.name() for lemma in s.lemmas()]
                
            self._syonyms[syn] = lemmas
        except ValueError:
            print(syn + " : no synsets found")
            
    def get_synonym_adj(self, syn):
        if syn not in self._syonyms:
            self._load_wn_adj_synonyms(syn)
        
        return choice(self._syonyms[syn])
    
    def get_qualifier(self):
        return choice(wordlists.qualifiers)
    
    def get_age_range(self, age):
        nums = sorted(self.ages.keys())
        
        for x in nums:
            if age <= x:
                return self.ages[x]
        
        return 'twenties'
        
       

class NPHelper(object):
    def __init__(self):
        self.ec = ExpressionChooser()
        self.intro_desc_temp = [Template('$article $girth $noun, who was also $qualifier1 $height'), 
                               Template('$article $height, $qualifier1 $girth $noun'),
                               Template('$article $qualifier1 $girth and $qualifier2 $height $noun in $poss $age'),
                                Template('$article $height, $girth $noun in $poss $age')]
    
    def pronoun(self, entity, case=None):
        if type(entity) is not bc.Person:
            return 'it'   
        elif entity.gender == 'male':
            if case == 'acc':
                return 'him'
            elif case == 'poss':
                return 'his'
            else:
                return 'he'
        else:
            if case == 'acc':
                return 'her'
            elif case == 'poss':
                return 'her'
            else:
                return 'she'
            
    def name(self, person):
        return person.noun
            
    def describe(self, person):
        atts = person.get_all_attributes()
        atts['article'] = 'a'
        atts['qualifier1'] = self.ec.get_qualifier()
        atts['qualifier2'] = self.ec.get_qualifier()
        atts['height'] = self.ec.get_synonym_adj(atts['height'])
        atts['girth'] = self.ec.get_synonym_adj(atts['girth'])
        atts['poss'] = self.pronoun(person, 'poss')
        atts['age'] = self.ec.get_age_range(atts['age'])
        temp = choice(self.intro_desc_temp)
        return temp.safe_substitute(atts)
    
    def intro_describe(self, person):
        s = self.describe(person)
        return person.noun + ", " + s
