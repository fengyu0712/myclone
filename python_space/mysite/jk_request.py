import requests
import json


class cls_api:
    def post(self, url, par):
        a_url = url
        a_par = par
        res = requests.post(a_url, a_par)
        return res

    def get(self, url, par):
        a_url = url
        a_par = par
        res = requests.get(a_url, a_par)
        return res