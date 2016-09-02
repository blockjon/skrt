import mock

from app import poller
from app.poller import poll


class TestPoller(object):

    def setup(self):
        poller.cars_outside_geofence = set([])

    def teardown(self):
        poller.cars_outside_geofence = set([])

    @mock.patch('app.poller.sleep_jitter')
    @mock.patch('app.poller.is_car_within_geofence', return_value=True)
    @mock.patch('app.poller.handle_car_within_geofence')
    def test_poll_forget(self, f, i, j):
        poll(1)
        f.assert_called_once_with(1)

    @mock.patch('app.poller.sleep_jitter')
    @mock.patch('app.poller.is_car_within_geofence', return_value=False)
    @mock.patch('app.poller.handle_car_outside_geofence')
    def test_poll_handle_car_outside_geofence(self, h, i, j):
        poll(1)
        h.assert_called_once_with(1)

    def test_forget(self):
        poller.cars_outside_geofence.add(1)
        poller.cars_outside_geofence.add(2)
        poller.cars_outside_geofence.add(3)
        poller.handle_car_within_geofence(3)
        assert 1 in poller.cars_outside_geofence
        assert 2 in poller.cars_outside_geofence
        assert 3 not in poller.cars_outside_geofence

    @mock.patch('app.poller.email_alert_team')
    def handle_car_outside_geofence(self, e):
        poller.handle_car_outside_geofence(1)
        poller.handle_car_outside_geofence(1)
        e.assert_called_once_with(1)
        assert len(poller.cars_outside_geofence) == 1
