import logging

from gevent import spawn, sleep

from app import poller, settings

# Uncomment for verbose output while running.
# logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    print "Poller running..."
    while True:
        for id in xrange(1, settings.NUM_USERS + 1):
            logging.info("Spawning poller for car {}".format(id))
            spawn(poller.poll, id)
        logging.info("Beginning sleep in main event loop for {} seconds".format(settings.SLEEP_INTERVAL))
        sleep(settings.SLEEP_INTERVAL)
