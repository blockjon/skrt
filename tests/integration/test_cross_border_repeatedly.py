import mock

from app import poller


class TestCrossBorderRepeatedly(object):

    def setup(self):
        poller.cars_outside_geofence = set([])

    def teardown(self):
        poller.cars_outside_geofence = set([])

    @mock.patch('app.poller.sleep_jitter')
    @mock.patch('app.poller.is_car_within_geofence', return_value=True)
    @mock.patch('app.poller.email_alert_team')
    def test_expected_behavior(self, e, i, s):
        car_id = 1

        # Car within geofence.
        poller.poll(car_id)

        e.assert_not_called()

        # Now the car is outside the geofence.
        i.return_value = False

        # Two samples indicate the car is outside the geofence.
        poller.poll(car_id)
        poller.poll(car_id)

        # Only one email should have triggered.
        e.assert_called_once()

        # The car travels back within the geofence...
        i.return_value = True

        # More samples are taken.
        poller.poll(car_id)
        poller.poll(car_id)

        # Still, we should have only ever sent one alert email
        e.assert_called_once()

        # Image the car goes back out beyond perimeter...
        i.return_value = False

        # More samples are taken.
        poller.poll(car_id)
        poller.poll(car_id)

        # Ensure that by this stage, only 2 alert emails have ever been sent.
        assert e.call_count == 2
