"""Parse size notations."""

import re

from traiter.util import to_positive_float

from ..pylib.consts import GROUP_STEP, NUMBER, PARTS, REPLACE, SLASH, TRAIT_STEP

SIZE_KEY = """ size """.split()
PLUS = """ bigger larger greater """.split()
LABELS = {
    1: ['low'],
    2: ['low', 'high'],
    3: ['min', 'low', 'high'],
    4: ['min', 'low', 'high', 'max'],
}


def measurement(span):
    """Enrich the match."""
    value = [to_positive_float(t.text) for t in span
             if re.match(NUMBER, t.text)]

    units = [REPLACE.get(t.lower_, t.lower_) for t in span
             if t.ent_type_ == 'length_units']

    data = {'value': value[0], 'units': units[0]}

    if any(t.lower_ in PLUS for t in span):
        data['plus'] = True

    return data


def size(span):
    """Enrich the match."""
    data = {}

    dim = 'length'

    measurements = [t._.data for t in span if t.ent_type_ == 'measurement']

    # Are all units the same?
    all_units = {m['units'] for m in measurements}
    if len(all_units) == 1:
        key = f'{dim}_units'
        data[key] = all_units.pop()

    low = ''
    for measure, lab in zip(measurements, LABELS[len(measurements)]):
        label = f'{dim}_{lab}'

        if lab == 'low':
            low = label

        if lab != 'high':
            data[label] = measure['value']

        # Handle cases where low == high or low > high
        else:
            if data[low] < measure['value']:
                data[label] = measure['value']
            elif data[low] > measure['value']:
                data[low], data[label] = measure['value'], data[low]

        if b := measure.get('plus'):
            data['plus'] = b

    if field := [t.lower_ for t in span if t.ent_type_ == 'part']:
        data['part'] = field[0]
    if field := [t.lower_ for t in span if t.ent_type_ == 'subpart']:
        data['subpart'] = field[0]

    return data


SIZE = {
    GROUP_STEP: [
        {
            'label': 'measurement',
            'on_match': measurement,
            'patterns': [
                [
                    {'POS': {'IN': ['ADJ', 'ADP']}, 'OP': '?'},
                    {'POS': 'SCONJ', 'OP': '?'},
                    {'TEXT': {'REGEX': NUMBER}},
                    {'ENT_TYPE': 'length_units'},
                ],
            ],
        },
    ],
    TRAIT_STEP: [
        {
            'label': 'size',
            'on_match': size,
            'patterns': [
                [
                    {'LOWER': {'IN': SIZE_KEY}},
                    {'POS': 'ADP', 'OP': '?'},
                    {'POS': 'DET', 'OP': '?'},
                    {'ENT_TYPE': {'IN': PARTS}},
                    {'ENT_TYPE': 'measurement'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'measurement', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'measurement', 'OP': '?'},
                    {'TEXT': {'IN': SLASH}, 'OP': '?'},
                    {'ENT_TYPE': 'measurement', 'OP': '?'},
                ],
            ],
        },
    ],
}
