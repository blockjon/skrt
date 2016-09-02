from app.poller import car_point_intersects_geofence, Point

TEST_GEOFENCE_ID = "90861196202500256"


def test_point_within_geofence():
    """ Ensure geofence point in polygon integration works. """
    assert car_point_intersects_geofence(
        Point(-118.4791374206543, 34.02677043872617),
        geofence_id=TEST_GEOFENCE_ID
    )


def test_point_outside_geofence():
    """ Ensure geofence point outside polygon integration works. """
    assert car_point_intersects_geofence(
        Point(-118.41922760009766, 34.07086232376631),
        geofence_id=TEST_GEOFENCE_ID
    ) is False
