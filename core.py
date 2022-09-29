
import requests
import json
import pandas as pd

url = 'https://api.monday.com/v2'
headers = {"Content-Type": "application/json", "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjE4MzM0NDM1OCwidWlkIjozNTEyMjUwNiwiaWFkIjoiMjAyMi0wOS0yOFQwOTo0ODoyMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTM1MjA0NTIsInJnbiI6ImV1YzEifQ.y_BZ8g9ltNENRM37XiRZ3ax5CHPJLNYx6vfxKwD7lJs"}


# SETUP
def getRoleSettings(role):
    print("Getting role settings...")

    query = """query {
        boards(ids: [1129937619]) {

            items {
              name
              column_values(ids: ["testo", "testo8"]) {
                title
                text
              }
            }
          }
        }"""

    r = requests.post(url, headers=headers, json={'query': query})
    res = json.loads(r.text)

    for r in res["data"]["boards"][0]["items"]:
        if r["name"] == role:
            final_res = {
                "esito": 0,
                "messaggio": r["column_values"][0]["text"],
                "parole_escluse": r["column_values"][1]["text"]
            }
            return final_res

    no_found = { "esito": 1 }
    return no_found


# SAVE CONTACTED PERSON
def insertContactedPerson(nomeCompleto, ruolo, account):
    query = """mutation($nomeCompleto: String!) {
          create_item(board_id: 1129971142, item_name: $nomeCompleto) {
            id
          }
        }"""

    variables = {'nomeCompleto': nomeCompleto}
    r = requests.post(url, headers=headers, json={'query': query, 'variables': variables})
    res = json.loads(r.text)

    id = res["data"]["create_item"]["id"]

    query1 = """mutation($itemId: Int!, $role: String!) {
          change_simple_column_value(item_id: $itemId, board_id: 1129971142, column_id: "testo", value: $role) {
            id
          }
        }"""

    variables = {'itemId': int(id), 'role': ruolo}
    r = requests.post(url, headers=headers, json={'query': query1, 'variables': variables})

    query2 = """mutation($itemId: Int!, $account: String!) {
          change_simple_column_value(item_id: $itemId, board_id: 1129971142, column_id: "testo2", value: $account) {
            id
          }
        }"""

    variables = {'itemId': int(id), 'account': account}
    r = requests.post(url, headers=headers, json={'query': query2, 'variables': variables})


# CHECK IF SOMEONE HAS ALREADY BEEN CONTACTED
def hasBeenContacted(nome):

    query = """
        query {
            boards(ids: [1129971142]) {
                items {
                  name
                }
            }
        }
    """
    r = requests.post(url, headers=headers, json={'query': query})
    res = json.loads(r.text)
    for n in res["data"]["boards"][0]["items"]:
        if n["name"] == nome:
            return True
    return False


def getAllContactedUser():
    query = """
        query {
            boards(ids: [1129971142]) {
                items {
                  name
                }
            }
        }
    """

    names = []
    r = requests.post(url, headers=headers, json={'query': query})
    res = json.loads(r.text)
    print(res)
    for n in res["data"]["boards"][0]["items"]:
        names.append(n["name"])
    return names

print(hasBeenContacted('Antonio Lusco'))