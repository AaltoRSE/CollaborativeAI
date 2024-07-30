from noun_extraction.noun_extraction import GetNoun
noun = GetNoun()
theme = 'summer'
sentence_entities_nouns = noun.getSimilarity(theme, [ 'spring is a good weather', 'I like dog', 'There\'s a bunch of white dogs'])
print(sentence_entities_nouns)