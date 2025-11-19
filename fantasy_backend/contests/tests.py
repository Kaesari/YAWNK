# from django.test import TestCase
# from django.contrib.auth.models import User
# from .models import Contest, Player, Team

# class ContestModelTest(TestCase):
#     def setUp(self):
#         self.contest = Contest.objects.create(
#             name="Test Contest",
#             sport="Football",
#             entry_fee=10.00,
#             prize_pool=100.00,
#             start_date="2025-01-10"
#         )

#     def test_contest_creation(self):
#         self.assertEqual(self.contest.name, "Test Contest")
#         self.assertEqual(self.contest.sport, "Football")

# class PlayerModelTest(TestCase):
#     def setUp(self):
#         self.player = Player.objects.create(
#             name="Test Player",
#             position="Forward",
#             team="Test Team",
#             score=5
#         )

#     def test_player_creation(self):
#         self.assertEqual(self.player.name, "Test Player")
#         self.assertEqual(self.player.score, 5)



# from django.urls import reverse

# class ContestViewTest(TestCase):
#     def setUp(self):
#         self.contest = Contest.objects.create(
#             name="Test Contest",
#             sport="Football",
#             entry_fee=10.00,
#             prize_pool=100.00,
#             start_date="2025-01-10"
#         )

#     def test_contest_list_view(self):
#         response = self.client.get(reverse('contest_list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Contest")

#     def test_contest_detail_view(self):
#         response = self.client.get(reverse('contest_detail', args=[self.contest.id]))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Test Contest")



# from rest_framework.test import APITestCase
# from rest_framework import status
# from .models import Contest, Player

# class APITests(APITestCase):
#     def setUp(self):
#         self.contest = Contest.objects.create(
#             name="API Contest",
#             sport="Football",
#             entry_fee=10.00,
#             prize_pool=100.00,
#             start_date="2025-01-10"
#         )

#     def test_get_contests(self):
#         response = self.client.get('/api/contests/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertContains(response, "API Contest")

#     def test_create_team(self):
#         response = self.client.post('/api/teams/', {
#             "user": 1,
#             "contest": self.contest.id,
#             "players": []
#         })
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
