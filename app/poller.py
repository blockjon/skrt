import random
import gevent
import logging
import requests
from collections import namedtuple

from app import settings

Point = namedtuple('Point', ['lng', 'lat'])

# Remember which vehicles are outside the geofence that we have already alerted on.
cars_outside_geofence = set([])


def is_car_within_geofence(car_id):
    point = get_car_location(car_id)
    return car_point_intersects_geofence(point)


def car_point_intersects_geofence(point, geofence_id=None):
    if not geofence_id:
        geofence_id = settings.GEOFENCE_ID
    result = requests.get(
        "{}/v1/query/{}?lat={}&lng={}".format(
            settings.GEOFENCE_SERVER,
            geofence_id,
            point.lat,
            point.lng
        ),
        headers={
            "AuthToken": settings.GEOFENCE_TOKEN
        },
        timeout=settings.GEOFENCE_SERVER_TIMEOUT
    )
    if result.status_code not in [200, 404]:
        raise Exception("Unexpected response from GeofenceAPI server. Status {} returned with body: {}".format(
            result.status_code,
            result.text
        ))
    return result.status_code == 200


def get_car_location(car_id):
    result = requests.get(
        "{}/carStatus/{}".format(settings.STATUS_SERVER, car_id),
        timeout=settings.STATUS_SERVER_TIMEOUT
    )
    for feature in result.json()['features']:
        if feature['geometry']['type'] == 'Point':
            coords = feature['geometry']['coordinates']
            return Point(
                lng=coords[0],
                lat=coords[1]
            )
    raise Exception("Could not detect point for car {}".format(car_id))


def sleep_jitter(seconds):
    # Allow other concurrent greenlets to continue while I sleep.
    gevent.sleep(seconds)


def email_alert_team(message):
    # No sense in sending real emails. Substituting with a print statement.
    # TODO: Use email solution to send email to "engineering@skurtapp.com"
    logging.info("(Pretend email send here) {}".format(message))


def handle_car_within_geofence(car_id):
    cars_outside_geofence.discard(car_id)


def handle_car_outside_geofence(car_id):
    if car_id not in cars_outside_geofence:
        cars_outside_geofence.add(car_id)
        email_alert_team("Alert! - Car #{} has gone beyond the allowed geofence.".format(car_id))


def poll(car_id):
    sleep_seconds = random.randrange(settings.POLL_DELAY_MAX_JITTER)
    logging.info("poll() handler for car {} will sleep_jitter for {} seconds".format(
        car_id, sleep_seconds
    ))
    sleep_jitter(sleep_seconds)

    logging.info("Examining location for car {}".format(car_id))

    try:
        car_within_geofence = is_car_within_geofence(car_id)
    except Exception as e:
        # Overly naive. I would rather log and let something like PagerDuty alert based on deduplicated log entries.
        message = "Failed to determine if vehicle {} is within the geofence. Exception: {}".format(
            car_id,
            e.message
        )
        logging.error(message)
        email_alert_team(message)
        return

    if car_within_geofence:
        handle_car_within_geofence(car_id)
    else:
        handle_car_outside_geofence(car_id)
