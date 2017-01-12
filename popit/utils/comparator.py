import requests
import logging

id_not_exists = set()

def comparator(entities):

    src_url = "http://sinar-malaysia.popit.mysociety.org/api/v0.1/%s/" % entities
    dst_url = "http://api.popit.sinarproject.org/en/%s/" % entities
    have_next = True

    while have_next:
        src = requests.get(src_url)
        data = src.json()
        results = data["result"]

        for result in results:

            d = requests.get("%s%s/" % (dst_url, result["id"]))
            if d.status_code == "404":
                logging.warn("%s %s not exist" % (entities, result["id"]))
                id_not_exists.add((result["id"], entities))

        if data["has_more"]:
            src_url = data["next_url"]
            have_next = True
        else:
            have_next = False
            break


def main():
    entities = [ "persons", "organizations", "posts", "memberships" ]
    for entity in entities:
        comparator(entity)
    print(id_not_exists)

if __name__ == "__main__":
    main()