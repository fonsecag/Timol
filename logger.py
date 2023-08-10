import logging 

logging.basicConfig(filename='log2.log', encoding='utf-8', level=logging.DEBUG)

with open("log.log", "w") as f:
    pass

def log_write(s):
    with open("log.log", "a") as log:
        log.write(str(s) + '\n')
    logging.info(str(s))

# log_file.close()