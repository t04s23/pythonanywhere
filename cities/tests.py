from django.test import Client, TestCase
from .models import City

# Create your tests here.
class CityViewTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        City.objects.create(
            city="Uruk",
            otherName='Eech',
            country='Iraq',
            latitude=31.322222,
            longitude=45.66099799,
            year=-3500,
            pop=14000,
            city_id='uruk.31.3_45.6',
        )
        City.objects.create(
            city="Uruk",
            otherName='Erech',
            country='Iraq',
            latitude=31.322222,
            longitude=45.66099799,
            year=-3000,
            pop=14500,
            city_id='uruk.31.3_45.6',
        )


        return super().setUpTestData()
    
    def test_index(self):
        client = Client()
        response = client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Historic")
            
    def test_cities(self):
        client = Client()
        response = self.client.get('/cities/Uruk')
        #print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is Uruk")