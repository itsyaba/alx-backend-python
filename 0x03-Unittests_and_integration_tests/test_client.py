#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([("google",), ("abc",)])
    @patch("client.get_json", return_value=org_payload)
    def test_org(self, org_name, mock_get_json):
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, org_payload)
        mock_get_json.assert_called_once_with(client.ORG_URL.format(org=org_name))

    def test_public_repos_url(self):
        with patch.object(GithubOrgClient, 'org', new_callable=property(lambda _: org_payload)):
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, org_payload["repos_url"])

    @patch("client.get_json", return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=property(lambda _: "url")):
            client = GithubOrgClient("testorg")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)

@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload,
     "expected_repos": expected_repos, "apache2_repos": apache2_repos},
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()
        mock_get.return_value.json.side_effect = [cls.org_payload, cls.repos_payload]

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
