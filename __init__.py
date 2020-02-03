import harmalysis.parsers.roman

def parse(query, syntax='roman'):
    if syntax == 'roman':
        roman = harmalysis.parsers.roman.parse(query, create_png=True)
        return roman