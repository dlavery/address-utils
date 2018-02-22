import unittest
from addressutils import single_line
from addressutils import normalise
from addressutils import separate_postcode
from addressutils import expand_abbreviations
from addressutils import remove_stopwords
from addressutils import strip_spaces
from addressutils import paf_to_lines
from addressutils import phonetic
from addressutils import jaccard_index

class TestAddressUtils(unittest.TestCase):

    def setUp(self):
        self.address = [' 3 The Brislee    Ave,', 'North    Shields', 'ne30 2sq']

    def test_single_line(self):
        res = single_line(self.address)
        self.assertEqual(res, ' 3 The Brislee    Ave, North    Shields ne30 2sq')

    def test_normalise(self):
        res = normalise(single_line(self.address))
        self.assertEqual(res, '3 THE BRISLEE AVE NORTH SHIELDS NE30 2SQ')

    def test_separate_postcode(self):
        res = separate_postcode(normalise(single_line(self.address)))
        self.assertEqual(res[0], '3 THE BRISLEE AVE NORTH SHIELDS')
        self.assertEqual(res[1], 'NE30 2SQ')

    def test_expand_abbreviations(self):
        res = expand_abbreviations(separate_postcode(normalise(single_line(self.address)))[0])
        self.assertEqual(res, '3 THE BRISLEE AVENUE NORTH SHIELDS')

    def test_remove_stopwords(self):
        res = remove_stopwords(expand_abbreviations(separate_postcode(normalise(single_line(self.address)))[0]))
        self.assertEqual(res, '3 BRISLEE AVENUE NORTH SHIELDS')

    def test_strip_spaces(self):
        res = strip_spaces(remove_stopwords(expand_abbreviations(separate_postcode(normalise(single_line(self.address)))[0])))
        self.assertEqual(res, '3BRISLEEAVENUENORTHSHIELDS')

    def test_paf_to_lines(self):
        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'dependentLocality': 'High Farm',
            'doubleDependentLocality': 'Kings Estate',
            'thoroughfare': 'Kings Road North',
            'dependentThoroughfare': 'Brand New Houses',
            'buildingNumber': '24',
            'buildingName': 'Block B',
            'subBuildingName': 'Flat 2',
            'organisationName': 'Bob The Builder'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], 'Bob The Builder')
        self.assertEqual(res[1], 'Flat 2 Block B')
        self.assertEqual(res[2], '24 Brand New Houses')
        self.assertEqual(res[3], 'Kings Road North')
        self.assertEqual(res[4], 'Kings Estate')
        self.assertEqual(res[5], 'High Farm')
        self.assertEqual(res[6], 'Wallsend')
        self.assertEqual(res[7], 'NE28 1AA')

        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'dependentLocality': 'High Farm',
            'thoroughfare': 'Kings Road North',
            'dependentThoroughfare': 'Brand New Houses',
            'buildingName': 'Block B',
            'subBuildingName': 'Flat 2',
            'organisationName': 'Bob The Builder'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], 'Bob The Builder')
        self.assertEqual(res[1], 'Flat 2 Block B')
        self.assertEqual(res[2], 'Brand New Houses')
        self.assertEqual(res[3], 'Kings Road North')
        self.assertEqual(res[4], 'High Farm')
        self.assertEqual(res[5], 'Wallsend')
        self.assertEqual(res[6], 'NE28 1AA')

        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'dependentLocality': 'High Farm',
            'doubleDependentLocality': 'Kings Estate',
            'thoroughfare': 'Kings Road North',
            'dependentThoroughfare': 'Brand New Houses',
            'buildingNumber': '24',
            'subBuildingName': 'Flat 2'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], 'Flat 2 24 Brand New Houses')
        self.assertEqual(res[1], 'Kings Road North')
        self.assertEqual(res[2], 'Kings Estate')
        self.assertEqual(res[3], 'High Farm')
        self.assertEqual(res[4], 'Wallsend')
        self.assertEqual(res[5], 'NE28 1AA')

        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'thoroughfare': 'Kings Road North',
            'buildingNumber': '24',
            'buildingName': 'Block B'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], 'Block B')
        self.assertEqual(res[1], '24 Kings Road North')
        self.assertEqual(res[2], 'Wallsend')
        self.assertEqual(res[3], 'NE28 1AA')

        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'thoroughfare': 'Kings Road North',
            'buildingName': 'Block B'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], 'Block B')
        self.assertEqual(res[1], 'Kings Road North')
        self.assertEqual(res[2], 'Wallsend')
        self.assertEqual(res[3], 'NE28 1AA')

        address = {
            'postcode': 'NE28 1AA',
            'postTown': 'Wallsend',
            'thoroughfare': 'Kings Road North',
            'buildingNumber': '24'
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], '24 Kings Road North')
        self.assertEqual(res[1], 'Wallsend')
        self.assertEqual(res[2], 'NE28 1AA')

        address = {
            'postTown': 'Wallsend',
            'thoroughfare': 'Kings Road North',
            'buildingNumber': '24',
            }
        res = paf_to_lines(address)
        self.assertEqual(res[0], '24 Kings Road North')
        self.assertEqual(res[1], 'Wallsend')

    def test_phonetic(self):
        self.assertEqual(phonetic('24 Kings Road North'), '24KNKSRTNR0')
        self.assertEqual(phonetic('Flat 3 Building B Kings Road North'), 'FLT3BLTNKBKNKSRTNR0')
        self.assertEqual(phonetic('3B 22 Kings Road North Wallsend'), '3B22KNKSRTNR0WLSNT')

    def test_jaccard_index(self):
        a1 = strip_spaces(remove_stopwords(expand_abbreviations(normalise('Flat 22, 8 St. Andrews Cross, PLYMOUTH'))))
        a2 = strip_spaces(remove_stopwords(expand_abbreviations(normalise('Flat 22, 8 St. Andrews Cross, PLYMOUTH'))))
        self.assertEqual(jaccard_index(a1, a2), 1)

        a3 = ''
        self.assertEqual(jaccard_index(a1, a3), 0)

        a4 = strip_spaces(remove_stopwords(expand_abbreviations(normalise('Flat 22, 8 St. Andrews Cross'))))
        self.assertGreater(jaccard_index(a1, a4), 0.7)

        a5 = strip_spaces(remove_stopwords(expand_abbreviations(normalise('Flat 22'))))
        self.assertLess(jaccard_index(a1, a5), 0.3)


if __name__ == '__main__':
    unittest.main()
