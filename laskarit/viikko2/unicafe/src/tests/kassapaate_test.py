import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_kassapaate_luotu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukas_kateisosto_toimii_jos_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(600)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_edullinen_kateisosto_toimii_jos_maksu_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(600)
        self.assertEqual(vaihtoraha, 360)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_maukas_kateisosto_ei_onnistu_jos_maksu_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassapaate.kassassa_rahaa)
        self.assertEqual(self.kassapaate.maukkaat, self.kassapaate.maukkaat)

    def test_edullinen_kateisosto_ei_onnistu_jos_maksu_ei_riittava(self):
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassapaate.kassassa_rahaa)
        self.assertEqual(self.kassapaate.edulliset, self.kassapaate.edulliset)

    def test_maukas_korttiosto_toimii_jos_saldo_riittava(self):
        kortti = Maksukortti(1000)
        res = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(res, True)
        self.assertEqual(str(kortti), "saldo: 6.0")
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassapaate.kassassa_rahaa)

    def test_edullinen_korttiosto_toimii_jos_saldo_riittava(self):
        kortti = Maksukortti(1000)
        res = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(res, True)
        self.assertEqual(str(kortti), "saldo: 7.6")
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, self.kassapaate.kassassa_rahaa)

    def test_maukas_korttiosto_ei_onnistu_jos_saldo_ei_riittava(self):
        kortti = Maksukortti(100)
        res = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(res, False)
        self.assertEqual(str(kortti), "saldo: 1.0")
        self.assertEqual(self.kassapaate.maukkaat, self.kassapaate.maukkaat)

    def test_edullinen_korttiosto_ei_onnistu_jos_saldo_ei_riittava(self):
        kortti = Maksukortti(100)
        res = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertEqual(res, False)
        self.assertEqual(str(kortti), "saldo: 1.0")
        self.assertEqual(self.kassapaate.edulliset, self.kassapaate.edulliset)

    def test_rahan_lataus_kasvattaa_kassan_ja_kortin_saldoa(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti, 1000)

        self.assertEqual(str(kortti), "saldo: 20.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 101000)

    def test_negatiivisen_summan_lataus_ei_onnistu(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti, -1000)

        self.assertEqual(str(kortti), "saldo: 10.0")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
