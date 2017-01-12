import requests
import logging

language_code = ["en", "ms"]
url = "http://sinar-malaysia.popit.mysociety.org/api/v0.1/%s/"
entities = [ "persons", "organizations", "posts", "memberships"]

def main():

    diff_dict = []

    for entity in entities:
        logging.warn("Processing entity %s" % entity)
        running = True
        url_ = url % entity
        while running:
            en_data = fetch_entity(url_, "en")
            ms_data = fetch_entity(url_, "ms")
            en_result = en_data["result"]
            ms_result = ms_data["result"]
            for item in range(len(en_result)):
                if en_result[item] != ms_result[item]:
                    logging.warn("%s id %s" % ( entity, en_result[item]["id"]))
                    diff_dict.append((en_result[item],ms_result[item]))
            if not en_data["has_more"]:
                running = False
            else:
                url_ = en_data["next_url"]

def fetch_entity(url, language):
    headers = { "Accept-Language": language }

    r = requests.get(url, headers=headers)
    return r.json()

if __name__ == "__main__":
    main()