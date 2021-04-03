import sys
sys.path.append("./libs/twint/")
import twint


c = twint.Config()
c.Username = "Piechocinski"
c.Store_json = True
c.Output = "janusz.json"
c.Lang = "pl"

twint.run.Search(c)