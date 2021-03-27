import sys
sys.path.append("./libs/twint/")
import twint


c = twint.Config()
c.Search = "koronawirus"
c.Store_json = True
c.Output = "corona.json"
c.Lang = "pl"

twint.run.Search(c)