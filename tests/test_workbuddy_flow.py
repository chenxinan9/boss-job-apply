"""Current WorkBuddy package contracts, not browser or BOSS acceptance."""
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class WorkBuddyFlowTest(unittest.TestCase):
    def test_business_flow_identical_and_no_private_defaults(self):
        texts=[(ROOT/'packages'/('boss-apply-workbuddy-'+s)/'SKILL.md').read_text(encoding='utf-8') for s in ('macos','windows')]
        self.assertEqual(*(t.split('## 先引导，后接管',1)[1] for t in texts))
        self.assertEqual(*((ROOT/'packages'/('boss-apply-workbuddy-'+s)/'BROWSER.md').read_text(encoding='utf-8') for s in ('macos','windows')))
        for t in texts:
            self.assertIn('BROWSER.md',t)
            for private in ('深圳','CMO','海外营销','/Users/','TaskSpace'):
                self.assertNotIn(private,t)

if __name__=='__main__':unittest.main()
