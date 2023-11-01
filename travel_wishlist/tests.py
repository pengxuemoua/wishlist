from django.test import TestCase
from django.urls import reverse

from .models import Place

class TestHomePage(TestCase):
    def test_home_page_shows_empty_list_message_for_empty_database(self):
        home_page_url = reverse('place_list') # turn place_list to an actually url
        response = self.client.get(home_page_url)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # template expected to be used
        self.assertContains(response, 'You have no places in your wishlist')

class TestWishList(TestCase):
    fixtures = ['test_places']

    def test_wishlist_contains_not_visited_places(self):
        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestVisitedPage(TestCase):
    def test_visited_page_shows_empty_list_message_for_empty_database(self):
        # visited_page_url = reverse('places_visited') 
        # response = self.client.get(visited_page_url)
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') 
        self.assertContains(response, 'You have not visited any places yet')

class TestVisitedList(TestCase):
    fixtures = ['test_places']

    def test_visted_page_contains_places_visted(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html')
        self.assertContains(response, 'San Francisco')
        self.assertContains(response, 'Moab')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestAddNewPlaces(TestCase):

    def test_add_new_unvisited_places(self):
        add_place_url = reverse('place_list')
        new_place_data = {'name': 'Tokyo', 'visited': False}
        
        response = self.client.post(add_place_url, new_place_data, follow=True)
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        response_places = response.context['places']
        self.assertEqual(1, len(response_places)) # checks only one place
        tokyo_from_response = response_places[0]

        tokyo_from_db = Place.objects.get(name='Tokyo', visited=False)

        self.assertEqual(tokyo_from_db, tokyo_from_response)


class TestVisitPlace(TestCase):

    fixtures = ['test_places']

    def test_visit_place(self):
        visited_place_url = reverse('place_was_visited', args=(2, ))
        response = self.client.post(visited_place_url, follow=True)

        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        self.assertNotContains(response, 'New York')
        self.assertContains(response, 'Tokyo')

        new_york = Place.objects.get(pk=2)
        self.assertTrue(new_york.visited)


    def test_non_existent_place(self):
        visit_nonexistent_place = reverse('place_was_visited', args=(26516, ))
        response = self.client.post(visit_nonexistent_place, follow=True)
        self.assertEqual(404, response.status_code)

