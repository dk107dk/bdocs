from application.roots.doc_root_management import DocRootManagement
from bdocs.bdocs_config import BdocsConfig
from application.app_config import AppConfig
import unittest
import os
import shutil

class DocRootManagementTests(unittest.TestCase):

    noise = BdocsConfig().get("testing", "DocRootManagementTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "DocRootManagementTests") == "off"

    def test_get_paths(self):
        self._print(f"DocRootManagementTests.test_get_paths")
        if self._off(): return

        cfg = AppConfig()
        ur_root = cfg.get("ur","root")
        self.assertIsNotNone(ur_root, msg=f"ur.root must not be None")
        home = ur_root + os.sep + "a/b/abcdefg"
        exists = os.path.exists(home)
        self.assertNotEqual(True, exists, msg=f"home {home} must not exist")

        mgmt = DocRootManagement()

        home = mgmt.finder.get_home_path("abcdefg")
        self._print(f"DocRootManagementTests.test_get_paths: home: {home}")
        exists = os.path.exists(home)
        self.assertEqual(True, exists, msg=f"home {home} must exist")

        team = mgmt.finder.get_team_path("abcdefg", "ateam")
        self._print(f"DocRootManagementTests.test_get_paths: team: {team}")
        exists = os.path.exists(team)
        self.assertEqual(True, exists, msg=f"team {team} must exist")

        project = mgmt.finder.get_project_path("abcdefg", "ateam", "aproject")
        self._print(f"DocRootManagementTests.test_get_paths: project: {project}")
        exists = os.path.exists(project)
        self.assertEqual(True, exists, msg=f"project {project} must exist")

        shutil.rmtree(home)
        exists = os.path.exists(home)
        self.assertNotEqual(True, exists, msg=f"home {home} must not exist")

    def test_get_config_of(self):
        self._print(f"DocRootManagementTests.test_get_config_of")
        if self._off(): return
        mgmt = DocRootManagement()
        account = "account1"
        team = "team1"
        project = "project1"
        cfg = mgmt.get_config_of(account, team, project)
        self.assertIsNotNone(cfg, msg=f"config of {account}, {team}, {project} must not be None")

        cfg = AppConfig()
        ur_root = cfg.get("ur","root")
        self.assertIsNotNone(ur_root, msg=f"ur.root must not be None")
        home = ur_root + os.sep + "a/c/account1/team1/project1"

        t = os.path.exists(home)
        self.assertEqual(t, True, msg=f"home dir {home} does not exist")

        t = os.path.exists(home + os.sep + "config/config.ini")
        self.assertEqual(t, True, msg=f"config/config.ini does not exist")

        t = os.path.exists(home + os.sep + "docs/default/404.xml")
        self.assertEqual(t, True, msg=f"404.xml does not exist")

        t = os.path.exists(home + os.sep + "tmp")
        self.assertEqual(t, True, msg=f"tmp dir does not exist")

        shutil.rmtree(home)
        exists = os.path.exists(home)
        self.assertNotEqual(True, exists, msg=f"home {home} must not exist")











