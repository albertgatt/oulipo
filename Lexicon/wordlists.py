'''
Created on 18 Sep 2015

@author: albertgatt
'''
from string import Template
from random import shuffle, choice 
import datetime

time1 = Template('It was $PERIOD in $MONTH.')
time2 = Template('One $PERIOD in $MONTH,')
times = [time1, time2]

char_appositive = Template('$NAME, $DESCRIPTION,')
char_descriptive = Template('$DESCRIPTION,')
char_relative = Template('$NAME, who was $DESCRIPTION,')

human_description = Template("a $ADJ $NOUN in $PRONOUN $AGE")

char_descriptions = [char_appositive, char_descriptive, char_relative]

state_desc1 = Template('was $ACTIVITY in $LOCATION when $TEMPCONJ')
state_desc2 = Template('had just finished $ACTIVITY in $LOCATION when $TEMPCONJ')
state_desc3 = Template('had just finished $ACTIVITY in $LOCATION. $TEMPCONJ, ')

state_descriptions = [state_desc1, state_desc2, state_desc3]

located_occurrence = Template('$NAME $ACTION $DESTINATION')
unlocated_occurrence = Template('$NAME $ACTION')

occurrences = [located_occurrence, unlocated_occurrence]

reaction1 = Template('$NAME $ACTION $DESCRIPTOR')


direct_speech1 = Template('"$STATEMENT", $PRONOUN said.')

time1 = Template('It was $PERIOD in $MONTH.')
    
# Season variations
spring = ['warm', 'fine']
winter = ['freezing', 'cold', 'chilly']
autumn = ['rainy', 'grey']
summer = ['hot', 'sultry']

# time periods
times = [0, 5, 8, 12, 17, 20, 22, 24]
periods = [Template('$ADJ in the dead of night'), Template('early one $ADJ morning'), Template('a $ADJ morning'), Template('a $ADJ afternoon'), Template('a $ADJ evening'), Template('a $ADJ night')]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#time expressions
temporal_conjunctions = ['suddenly', 'just then', 'all of a sudden', 'with a loud noise', 'with considerable stealth']
flashback_conjunctions = ['a few days before', 'just the previous day', 'many years before', 'a couple of hours before']
switchback_conjunctions = ['now', 'at present', 'at this moment']
flashforward_conjunctions = ['later', 'the next day', 'some time later', 'not long after', 'soon', 'a few days later', 'subsequently']
    
male_names = ['Abdallah', 'Abdel-Rahman', 'Abi', 'Abinet', 'Abraham', 'Ahmed', 'Ali', 'Amanual', 'Araya', 'Asfaw', 'Bereket', 'Berhane', 'Bilal', 'Biniam', 'Biruk', 'Daniel', 'Dawit', 'Derege', 'Elias', 'Ephrem', 'Ermias', 'Eyobel', 'Ezra', 'Fasil', 'Gebre', 'Haile', 'Halim', 'Hamza', 'Hanok', 'Hassan', 'Hewan', 'Hussein', 'Ibrahim', 'Karim', 'Khaled', 'Kidus', 'Kirubel', 'Mahmoud', 'Mathios', 'Melak', 'Mohammed', 'Murad', 'Mustafa', 'Nahum', 'Omar', 'Robel', 'Selim', 'Shewit', 'Tadesse', 'Taha', 'Tamiru', 'Tamrat', 'Tareq', 'Teodros', 'Yared', 'Yassin', 'Yonas', 'Yordanos', 'Youssef', 'Zecharias', 'An', 'Bo', 'Cheng', 'De', 'Dong', 'Feng', 'Gang', 'Guo', 'Hui', 'Jian', 'Jie', 'Kang', 'Liang', 'Ning', 'Peng', 'Tao', 'Wei', 'Yong', 'Wen', 'Alexander', 'Sergei', 'Dmitry', 'Andrei', 'Alexey', 'Maxim', 'Evgeny', 'Ivan', 'Mikhail', 'Artyom', 'Bill', 'Jim', 'Nick', 'Darius', 'Leonardo', 'Scott', 'Christian', 'Darren', 'Kenny', 'Brad', 'Zenon']
shuffle(male_names)

female_names = ['Abeba', 'Alem', 'Almaz', 'Ashraqat', 'Aya', 'Azeb', 'Bethlehem', 'Dalal', 'Desta', 'Doha', 'Eden', 'Elsa', 'Fajr', 'Farida', 'Fatima', 'Fatin', 'Fatma', 'Feven', 'Gamalat', 'Gamila', 'Haben', 'Habiba', 'Hasnaa', 'Helen', 'Hosna', 'Hosniya', 'Jerusalem', 'Kedist', 'Leah', 'Lili', 'Luwam', 'Lydia', 'Maha', 'Mahlet', 'Manna', 'Marone', 'Messeret', 'Rahiel', 'Reem', 'Rowan', 'Ruth', 'Saba', 'Sahar', 'Samrawit', 'Sara', 'Senait', 'Shahd', 'Shaimaa', 'Shewit', 'Suha', 'Tigist', 'Tizita', 'Tsega', 'Tsege', 'Yeshi', 'Yohana', 'Zewdy', 'Ai', 'Bi', 'Cai', 'Dan', 'Fang', 'Hong', 'Hui', 'Juan', 'Lan', 'Li', 'Lian', 'Na', 'Ni', 'Qian', 'Qiong', 'Shan', 'Shu', 'Ting', 'Xia', 'Xian', 'Yan', 'Yun', 'Zhen', 'Anastasia', 'Yelena', 'Olga', 'Natalia', 'Yekaterina', 'Anna', 'Tatiana', 'Maria', 'Irina', 'Yulia', 'Jennifer', 'Katie', 'Ali', 'Buffy', 'Christie', 'Stephanie', 'Vanessa', 'Johanna', 'Amaranth', 'Jill', 'Katarzyna']
shuffle(female_names) 

#Human attributes
qualifiers = ['somewhat', 'rather', 'very', 'extremely', 'slightly']
human_descriptor = ['fat', 'plump', 'diminutive', 'tall', 'short', 'rotund']
girth_synsets = ['fat.a.01', 'thin.a.01']
height_synsets = ['tall.a.01', 'short.a.01']


activities = ['sit', 'read', 'eat', 'sleep', 'clean', 'write', 'lounge', 'pass the time', 'while away the time', 'waste time']
temporal_conjunctions = ['out of nowhere', 'without warning', 'suddenly', 'just then', 'all of a sudden', 'with a loud noise', 'with considerable stealth']
locations = ['sitting room', 'bathroom', 'study', 'bedroom', 'garden']
actions = ['walk', 'creep', 'rush', 'step', 'march', 'pop', 'crawl', 'roll', 'call']
reactons = ['give a start', 'sit up', 'blink', 'jump', 'yelp', 'sit back']
reaction_descriptors = ['in surprise', 'with a start', 'in a tizzy', 'with a thumping heart', 'like a shot']
unlocated_occurrences = ['wave', 'smile', 'grimace', 'chuckle', 'smirk', 'burst into tears', 'tremble', 'shiver', 'shudder']
statements = ['OK', 'as you wish', 'I will', 'I won\'t', 'I agree', 'I disagree', 'no way', 'not a chance', 'fat chance', 'forget it', 'I suppose we can']

#Communication
comm_verbs = ['call', 'telephone', 'text', 'email', 'send word', 'send a telegram', 'send an envoy', 'send a messenger', 'send a carrier pigeon', 'send an emissary', 'write', 'write a letter', 'wire']
comm_objects = ['had some news', 'had an emergency', 'needed a friendly ear', 'required assistance']

weapons = ['gun', 'knife', 'broken bottle', 'shard of glass', 'dagger']

#Season variations
spring = ['warm', 'fine']
winter = ['freezing', 'cold', 'chilly']
autumn = ['rainy', 'grey']
summer = ['hot', 'sultry']

#time periods
times = [0, 5, 8, 12, 17, 20, 22, 24]
periods = [Template('$ADJ in the dead of night'), Template('early one $ADJ morning'), Template('a $ADJ morning'), Template('a $ADJ afternoon'), Template('a $ADJ evening'), Template('a $ADJ night')]
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


media = ['the papers', 'the radio', 'the television', 'the media', 'the social networks', 'the tabloids', 'Twitter', 'Facebook']

def random_get(choices):
    return choice(choices)








    
    
        

    
    
    
    
    
        
