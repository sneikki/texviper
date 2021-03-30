import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_on_oikein(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")

    def test_rahan_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(25)
        self.assertEqual(str(self.maksukortti), "saldo: 0.35")

    def test_ota_rahaa_toimii_oikein_jos_tarpeeksi_rahaa(self):
        res = self.maksukortti.ota_rahaa(3)
        self.assertEqual(str(self.maksukortti), "saldo: 0.07")
        self.assertEqual(res, True)

    def test_ota_rahaa_toimii_oikein_jos_ei_tarpeeksi_rahaa(self):
        res = self.maksukortti.ota_rahaa(22)
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")
        self.assertEqual(res, False)
