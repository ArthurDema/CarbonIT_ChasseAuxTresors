import unittest
from ChasseAuxTresors import Aventurier, Tresor, Mountain, Map, get_valid_argument, create_map, tour_par_tour

 
class TestMapFunctions(unittest.TestCase):
    def test_is_orientation(self):
        self.assertTrue(Aventurier.is_orientation(any,"D"), True)
        self.assertTrue(Aventurier.is_orientation(any, "G"), True)
        self.assertFalse(Aventurier.is_orientation(any, "A"), False)

    def test_create_map_valid_file(self):
        map_game = create_map("Cas_de_tests/Cas1.txt")
        self.assertIsNotNone(map_game)
        self.assertEqual(map_game.dimensionX, 3)
        self.assertEqual(map_game.dimensionY, 4)
        self.assertEqual(len(map_game.mountains), 2)
        self.assertEqual(len(map_game.tresors), 2)
        self.assertEqual(len(map_game.aventuriers), 1)

    def test_get_valid_argument(self):
        self.asse              
