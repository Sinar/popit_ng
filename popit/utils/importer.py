import requests
import logging

SOURCE="https://sinar-malaysia.popit.mysociety.org/api/v0.1/%s"
DEST="http://api.popit.sinarproject.org/%s/%s/"

logger = logging.getLogger("popit_importer")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("popit_importer.log")
file_handler.setLevel(logging.ERROR)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

BLACK_LIST = [
]

def migrator(source, destination, entity_key, language):

    source_header = { "Accept-Language": language}
    source_data = requests.get(SOURCE % entity_key, headers=source_header, verify=False)
    dest_header = { "Authorization":"Token 3e6a794d84fc00dc613f40e426cbc4f19b69a68e" }
    datas = source_data.json()
    while datas["has_more"]:
        for data in datas["result"]:
            logger.info("processing %s for id %s" % (entity_key, data["id"]))
            create_url = DEST % (language, entity_key)
            check_url = "%s%s/" % (create_url, data["id"])
            check = requests.get(check_url)
            if check.status_code == 404:
                logger.info(data)
                dest_data = requests.post(create_url, headers=dest_header, data=data)
                if dest_data.status_code != 201:
                    logger.error("entity: %s, id:%s, status_code:%s, error:%s" % (entity_key, data["id"], dest_data.status_code, dest_data.text))
                    continue
            else:
                logger.info("Status code is %s for %s" % (check.status_code, check_url) )
        source_data = requests.get(datas["next_url"], headers=source_header, verify=False)
        datas = source_data.json()
        logger.info("page number %s" % datas["page"])

def main():
    languages = ["en", ]
    entities = ["persons", "organizations", "posts", "memberships"]
    for language in languages:
        for entity in entities:
            logger.info("Migrating %s for %s" % (entity, language))
            migrator(SOURCE, DEST, entity, language)

if __name__ == "__main__":
    main()




