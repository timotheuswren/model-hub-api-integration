import pathlib,unittest
class T(unittest.TestCase):
 def test_boundary(self):
  s=pathlib.Path("README.md").read_text();self.assertIn("Last checked",s);self.assertIn("ArgoLink",s)
if __name__=="__main__":unittest.main()
