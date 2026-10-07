import json,pathlib,unittest
class T(unittest.TestCase):
 def test_unknowns_are_text(self):
  d=json.loads((pathlib.Path(__file__).parents[1]/"matrix/compatibility.json").read_text());self.assertIn("features",d);self.assertNotIn("true",str(d).lower())
if __name__=="__main__":unittest.main()
