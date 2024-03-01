import unittest
from bdocs.building_metadata import BuildingMetadata
from bdocs.bdocs_config import BdocsConfig
from bdocs.root_info import RootInfo
from cdocs.cdocs import Cdocs
from bdocs.bdocs import Bdocs
from bdocs.rules.rules import Rules
from bdocs.rules.rule import Rule
from bdocs.rules.rule_types import RuleTypes
import os
from datetime import datetime, timedelta

PATH = "/Users/davidkershaw/dev/bdocs/server/docs"
ROOTDIR = "example"
ROOTNAME = "public"
ROOT = PATH + "/" + ROOTDIR
RULE = "/app/home"

class RulesTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setting up RulesTests")
        BdocsConfig.setTesting()

    noise = BdocsConfig().get("testing", "RulesTests_noise") == "on"
    def _print(self, text:str) -> None:
        if self.noise:
            print(text)

    def _off(self):
        return BdocsConfig().get("testing", "RulesTests") == "off"

    def test_rules_feature(self):
        self._print(f"RulesTests.test_rules_feature")
        if self._off(): return
        metadata = BuildingMetadata()
        rootinfo = metadata.get_root_info(ROOTNAME)
        self.assertEqual(True, rootinfo.rules, msg=f"root {ROOTNAME} must have rules feature")

    def test_rules_root_dir(self):
        self._print(f"RulesTests.test_rules_feature")
        if self._off(): return
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        rules = Rules(cdocs)
        rulesroot = rules.get_rules_root()
        self._print(f"RulesTests.test_rules_root_dir: rulesroot: {rulesroot}")
        apath = f"{metadata.config.get('locations', 'docs_dir')}{os.sep}.{cdocs.rootname}_rules"
        exists = os.path.exists( apath )
        self.assertEqual(True, exists, msg=f"the rules directory for {ROOT} named {cdocs.rootname} must exist at {apath}")
        rules.delete_rules_root()
        exists = os.path.exists( apath )
        self.assertEqual(False, exists, msg=f"the rules directory must nolonger exist at {apath}")

    def test_rule_types(self):
        self._print(f"RulesTests.test_rules_from_to")
        if self._off(): return
        self.assertEqual(RuleTypes.REPLACE_AFTER.value, "replace_after",
                         msg=f"rule type 'RuleTypes.REPLACE.value' must be 'replace'")

    """
    # this test does nothing meaningful so I'm disabling it
    #
    def test_rules_from_to_action(self):
        self._print(f"RulesTests.test_rules_from_to_action")
        if self._off(): return
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        rules = Rules(cdocs)
        self._print(f"RulesTests.test_rules_from_to_action: rules: {rules}")
        rule = rules.new_rule()
        self._print(f"RulesTests.test_rules_from_to_action: rule: {rule}")
        at = datetime.now()
        rule.start_at = at
        self.assertEqual(True, rule.has_start_at(), msg=f"the rule must have a start_at")
        rule.to = at
        self.assertEqual(True, rule.has_to(), msg=f"the rule must have a to")
        rule.action = RuleTypes.SWAP
        self._print(f"RulesTests.test_rules_from_to_action: rule.action: {rule.action}")
        self.assertEqual("swap", rule.action.value, msg=f"the rule must have action 'swap', not {rule.action}")
    """

    def test_rule_started_ended_happening(self):
        self._print(f"RulesTests.test_rule_started_ended_happening")
        if self._off(): return
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, BdocsConfig())
        rules = Rules(cdocs)
        self._print(f"RulesTests.test_rule_started_ended_happening: rules: {rules}")
        rule = rules.new_rule()
        self._print(f"RulesTests.test_rule_started_ended_happening: rule: {rule}")
        at = datetime.now()
        self._print(f"RulesTests.test_rule_started_ended_happening: now: {at}")
        at = datetime(at.year, at.month, at.day, at.hour, at.minute -1, 10)
        self._print(f"RulesTests.test_rule_started_ended_happening: start at: {at}")
        rule.start_at = at
        started = rule.has_started()
        self.assertEqual(True, started, msg=f"the rule must have started")
        ended = rule.has_ended()
        self.assertEqual(False, ended, msg=f"the rule must not have ended")
        happening = rule.is_happening()
        self.assertEqual(True, happening, msg=f"the rule must be happening")
        at = datetime(at.year, at.month, at.day, at.hour, at.minute, 5 )
        self._print(f"RulesTests.test_rule_started_ended_happening: end at: {at}")
        rule.to = at
        started = rule.has_started()
        self.assertEqual(True, started, msg=f"the rule must have started")
        ended = rule.has_ended()
        self.assertEqual(True, ended, msg=f"the rule must have ended")
        happening = rule.is_happening()
        self.assertEqual(False, happening, msg=f"the rule must not be happening")

    def test_run_rule(self):
        self._print(f"RulesTests.test_run_rule")
        if self._off(): return
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        rules = Rules(cdocs)
        self._print(f"RulesTests.test_run_rule: rules: {rules}")
        rule = rules.new_rule()
        rule.docpath = RULE
        rule.action = RuleTypes.AVAILABLE_DURING
        self._print(f"test_run_rule: rule.action class: {rule.action.__class__}")
        n = datetime.now()
        n2 = n + timedelta(days=1)
        n = n + timedelta(days=-1)
        rule.start_at = n
        rule.to = n2
        rules.put_rule(rule)
        rule = rules.get_rule('/app/home')
        self.assertIsNotNone(rule, msg=f"rule_1: {RULE} must not be None")
        self._print(f"RulesTests.test_run_rule: rule: {rule} {rule.action} {rule.action.__class__}")
        assert isinstance(rule.action, RuleTypes)
        self.assertEqual(
                RuleTypes.AVAILABLE_DURING,
                rule.action, msg=f"rule: {RULE} {rule.action} action must be {RuleTypes.AVAILABLE_DURING}")
        rule.may_be_available()
        rules.delete_rule(rule)

    def test_crud_rule(self):
        self._print(f"RulesTests.test_crud_rule")
        if self._off(): return
        path = '/app/home/test'
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        self._print(f"RulesTests.test_crud_rule: ROOT: {ROOT}")
        rules = Rules(cdocs)
        self._print(f"RulesTests.test_crud_rule: rules: {rules}")
        rule = rules.new_rule()
        rule.docpath = path
        rule.action = RuleTypes.AVAILABLE_DURING
        rule.paths = ["/app/home","/app/fish"]
        rule.start_at = datetime.now()
        rule.to = datetime.now()
        self._print(f"RulesTests.test_crud_rule: rule: {rule}")
        string = rule.to_string()
        rules.put_rule(rule)
        rule = rules.get_rule(path)
        self.assertIsNotNone(rule, msg=f"rule must not be None")
        string2 = rule.to_string()
        self._print(f"RulesTests.test_crud_rule: string : {string}")
        self._print(f"RulesTests.test_crud_rule: string2: {string2}\n")
        self.assertEqual(string, string2, msg=f"rule: {rule}: string: {string}, string2: {string2} must be equal")
        rules.delete_rule(rule)
        self._print(f"RulesTests.test_crud_rule: deleted rule")
        rule = rules.get_rule(path)
        self.assertIsNone(rule, msg=f"rule must be None")


    def test_list_rules(self):
        self._print(f"RulesTests.test_list_rules")
        if self._off(): return
        path = '/app/home/test'
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        rules = Rules(cdocs)
        #
        # clear the rules tree completely
        #
        rules.delete_rules_root()
        rules = Rules(cdocs)

        self._print(f"RulesTests.test_list_rules: rules: {rules}")
        rule = rules.new_rule()
        rule.docpath = path
        rule.action = RuleTypes.AVAILABLE_DURING
        rule.paths = ["/app/home","/app/fish"]
        rule.start_at = datetime.now()
        rule.to = datetime.now()
        rules.put_rule(rule)
        rs = rules.list_rules()
        """
        found1 = False
        found2 = False
        for path in rs:
            self._print(f"RulesTests.test_list_rules: a path: {path}")
            #
            # why would we expect to find an html doc in the rules rdoc?

            if path == ".public_rules/app/home/home.html":
                found1 = True
            elif path == ".public_rules/app/home/test.rule":
                found2 = True
        """
        self.assertEqual(1, len(rs), msg=f"must be 1 rule in {rs}")
        self.assertEqual( True, ".public_rules/app/home/test.rule" in rs, msg=f".public_rules/app/home/test.rule not in {rs}")
        rules.delete_rule(rule)
        self._print(f"RulesTests.test_list_rules: deleted rule")
        rule = rules.get_rule(path)
        self.assertIsNone(rule, msg=f"rule must be None")


    def test_work_the_rule(self):
        self._print(f"RulesTests.test_work_the_rule")
        if self._off(): return
        path = '/app/home'
        yesterday = datetime.now() + timedelta(days=-1)
        tomorrow = datetime.now() + timedelta(days=1)
        thefollowingday = datetime.now() + timedelta(days=2)
        #
        # setup
        #
        metadata = BuildingMetadata()
        cdocs = Cdocs(ROOT, metadata.config)
        create = f"{ROOT}{path}.xml"
        with open(create, "w") as f:
            f.write("this is home")

        rules = Rules(cdocs)
        self._print(f"RulesTests.test_work_the_rule: rules: {rules}")
        rule = rules.new_rule()
        rule.docpath = path
        rule.action = RuleTypes.AVAILABLE_DURING
        rule.paths = ["/app/home/teams/todos","/app/home/teams/todos/assignee"]
        rule.start_at = yesterday
        rule.to = tomorrow
        self._print(f"RulesTests.test_work_the_rule: rule: {rule}")
        #
        # AVAILABLE_DURING
        #
        a = rule.may_be_available()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be available")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath {cdocs.rootname}:{rule.docpath} must not be None")
        found = doc.find("this is home") > -1
        self.assertEqual(found, True, msg=f"doc at rule docpath: {rule.docpath} must include 'this is home'")
        rule.start_at = tomorrow
        rule.to = thefollowingday
        doc = rule.get_doc()
        self.assertIsNone(doc, msg=f"doc at rule docpath: {rule.docpath} must be None")
        #
        # REPLACE_AFTER
        #
        rule.action = RuleTypes.REPLACE_AFTER
        rule.start_at = tomorrow
        rule.to = thefollowingday
        a = rule.is_happening()
        self.assertEqual(a, False, msg=f"rule: {rule}: must not be happening")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath: {rule.docpath} must not be None")
        found = doc.find("this is home") > -1
        self.assertEqual(found, True, msg=f"doc {doc} at rule docpath: {rule.docpath} must include 'this is home'")
        rule.start_at = yesterday
        rule.to = tomorrow
        a = rule.may_be_available()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be available")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath: {rule.docpath} must not be None")
        found = doc.find("my app name") > -1
        self.assertEqual(found, True, msg=f"doc {doc} at rule docpath: {rule.docpath} must include 'my app name'")
        #
        # REPLACE_UNTIL
        #
        rule.start_at = yesterday
        rule.to = tomorrow
        rule.action = RuleTypes.REPLACE_UNTIL
        a = rule.may_be_available()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be available")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath: {rule.docpath} must not be None")
        found = doc.find("my app name") > -1
        self.assertEqual(found, True, msg=f"doc at rule docpath: {rule.docpath} must include 'my app name'")
        #
        # RANDOM_AFTER
        #
        rule.action = RuleTypes.RANDOM_AFTER
        a = rule.may_be_available()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be available")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath: {rule.docpath} must not be None")
        found = doc.find("my app name") > -1
        found = found or doc.find("assignee in") > -1
        self.assertEqual(found, True, msg=f"doc at rule docpath: {rule.docpath} must include 'my app name' or 'assignee in'")
        #
        # RANDOM_UNTIL
        #
        rule.action = RuleTypes.RANDOM_UNTIL
        a = rule.may_be_available()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be available")
        doc = rule.get_doc()
        self.assertIsNotNone(doc, msg=f"doc at rule docpath: {rule.docpath} must not be None")
        found = doc.find("my app name") > -1
        found = found or doc.find("assignee in") > -1
        self.assertEqual(found, True, msg=f"doc at rule docpath: {rule.docpath} must include 'my app name' or 'assignee in'")
        #
        # UNAVAILABLE_DURING
        #
        rule.action = RuleTypes.UNAVAILABLE_DURING
        a = rule.is_happening()
        self.assertEqual(a, True, msg=f"rule: {rule}: must be happening")
        doc = rule.get_doc()
        self.assertIsNone(doc, msg=f"doc at rule docpath: {rule.docpath} must be None")
        #
        # UNAVAILABLE_AFTER
        #
        rule.action = RuleTypes.UNAVAILABLE_AFTER
        a = rule.has_started()
        self.assertEqual(a, True, msg=f"rule: {rule}: must have started")
        doc = rule.get_doc()
        self.assertIsNone(doc, msg=f"doc at rule docpath: {rule.docpath} must be None")
        #
        # UNAVAILABLE_BEFORE
        #
        rule.action = RuleTypes.UNAVAILABLE_BEFORE
        rule.start_at = datetime.now() + timedelta(days=+1)
        a = rule.has_started()
        self.assertEqual(a, False, msg=f"rule: {rule}: must not have started")
        doc = rule.get_doc()
        self.assertIsNone(doc, msg=f"doc at rule docpath: {rule.docpath} must be None")



