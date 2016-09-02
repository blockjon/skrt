from app.poller import get_car_location


def test_integration_with_car_status_server():
    """ Ensure scraping vehicle location appears to work. """
    point = get_car_location(1)
    assert type(point.lat) is float
