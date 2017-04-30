'''
Created on 15 Sep 2015

@author: albertgatt
'''

from enum import Enum
from string import Template
import collections
import datetime


class Roles(Enum):
    AGENT = 1
    THEME = 2
    PATIENT = 3
    LOCATION = 4
    UTTERANCE = 5    
    
class GrammaticalFunctions(Enum):
    SUBJECT = 1
    OBJECT = 2
    ADJUNCT = 3
    
class Tense(Enum):
    PRESENT = 1
    PAST = 2
    FUTURE= 3
    
class Aspect(Enum):
    SIMPLE = 1
    PROGRESSIVE = 2

        
class Entity(object):
    
    def __init__(self, role, noun, common=True):
        self._role = role
        self._noun = noun
        self._common = common
        self._common_template = Template('$DET $NOUN')
        self._attributes = dict()
      
    @property
    def role(self):
        '''Get the role assigned to this character'''
        return self._role  

    @property
    def noun(self):
        '''Get the noun corresponding to this entity'''
        return self._noun
    
    @property
    def common(self):
        '''Check if this is a common noun'''
        return self._common
    
    
    def add_attribute(self, attribute, value):
        self._attributes[attribute] = value
        
    def get_attribute(self, attribute):
        return self._attributes[attribute]    
    
    @property
    def attributes(self):
        return self._attributes
    
    def get_all_attributes(self):
        d = dict(self._attributes)
        d['noun'] = self._noun
        return d
    
    def get_attribute_string(self):
        return ','.join(x + ' ' + y for (y,x) in self._attributes.items())
    
    def make_referring_expression(self):
    
        if self._common:
            return self._common_template.substitute(DET="the", NOUN=self._noun)
        else:
            return self._noun


class Location(Entity):
    
    def __init__(self, noun, preposition="in"):
        super(Location, self).__init__(Roles.LOCATION, noun, True)
        self._preposition = preposition 
        
    @property
    def preposition(self):
        return self._preposition
    
    def make_referring_expression(self):
        
        if self._common:
            return self._preposition + ' ' + self._common_template.substitute(DET="the", NOUN=self._noun)
        else:
            return self._preposotion + self._noun


class Person(Entity):
    def __init__(self, role, name, gender, age):
        super(Person, self).__init__(role, name, False)
        self._gender = gender
        self._age = age
    
    @property
    def age(self):
        return self._age
    
    @property
    def gender(self):
        return self._gender
    
    def get_all_attributes(self):
        d = super().get_all_attributes()
        d['noun'] = self.get_common_noun()
        d['name'] = self.noun
        d['age'] = self.age
        return d
    
    def get_common_noun(self):
        if self._gender == 'male':
            return 'man'
        return 'woman'
    
    def is_male(self):
        return self._gender == 'male'
    
    def get_pronoun(self, type='nom'):
        if self.is_male():
            if type == 'acc':
                return 'him'
            elif type == 'poss':
                return 'his'
            else:
                return 'he'
        else:
            if type == 'acc':
                return 'her'
            elif type == 'poss':
                return 'her'
            else:
                return 'she'

class Event(object):
    
    def __init__(self, v, transitive=True):
        self._verb = v
        self._transitive = transitive
        self._args = dict()
        self._time = None
            
    @property
    def verb(self):
        return self._verb        
    
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, dt):
        if isinstance(dt, datetime.datetime):
            self._time = dt
    
    @property
    def Lexicon(self):
        '''Get the Lexicon corresponding to this event'''
        return self._verb
    
    @property
    def transitive(self):
        '''Check whether this event is transitive'''
        return self._transitive
    
    def add_arg(self, arg):
        self._args[arg.role] = arg
        
    def get_arg(self, role):
        if role in self._args:
            return self._args[role]
        return None
    
    def get_theme(self):
        return self.get_arg(Roles.THEME)
    
    def get_location(self):
        return self.get_arg(Roles.LOCATION)
    
    def get_utterance_arg(self):
        return self.get_arg(Roles.UTTERANCE)


class EventSchema(object):
    
    def __init__(self, event, *args ):
        self._event = event
        self._entities = args
        self._sentence_schema = SentenceSchema()
    
    @property
    def event(self):
        '''Retrieve the Event object in this event schema'''
        return self._event
    
    def has_oblique_role(self):
        '''Check if this event also has an oblique role'''
        return len(list(filter(lambda x: x.role == Roles.LOCATION, self._entities))) > 0
    
    @property
    def entities(self):
        '''Retrieve the arguments of the event'''
        return self._entities
    
    @property
    def sentence_schema(self):
        '''Get the sentence schema corresponding to this event'''
        return self._sentence_schema
    
    @sentence_schema.setter
    def sentence_schema(self, value):
        self._sentence_schema = value
        
    def default_schema(self):
        None
        
    def realise(self):
        return self._sentence_schema.render(self)
    
        
class SentenceSchema(object):
    
    def __init__(self, **functions):
        self._functions = functions
        self._trans_string = Template('$SUBJECT $VERB $OBJECT')
        self._intrans_string = Template('$SUBJECT $VERB')
        self._oblique_string = Template('$preposition $ADJUNCT')
        
    def render(self, event_schema):
        event = event_schema.event
        entities = event_schema.entities
        v = Lexicon.verb_past(event.verb)
        template = None
        oblique = event_schema.has_oblique_role()
        
        if event.transitive:
            template = self._trans_string
        else:
            template = self._intrans_string
        
        sentence_blocks = dict(VERB=v)
        
        for character in entities:
            r = character.role
            f = GrammaticalFunctions(r.value)
            n = character.make_referring_expression()
            sentence_blocks[f.name] = n
        
        if oblique:
            return template.substitute(sentence_blocks) + self._oblique_string.substitute(sentence_blocks)
        else: 
            return template.substitute(sentence_blocks)
        