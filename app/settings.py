# Main event loop sleep interval 2 minutes and 20 seconds
SLEEP_INTERVAL = 140

# Window of random jitter. Setting to 10 seconds less than SLEEP_INTERVAL to let any stragglers complete.
POLL_DELAY_MAX_JITTER = 130

# Number of simulated users
NUM_USERS = 11

# Host of the demo status server.
STATUS_SERVER = "http://skurt-interview-api.herokuapp.com"

# Give up waiting for car status after this many seconds
STATUS_SERVER_TIMEOUT = 5

# Give up waiting on geofence server after this many seconds.
GEOFENCE_SERVER_TIMEOUT = 5

# GeofenceAPI creds.
GEOFENCE_ID = 90932088932688036
GEOFENCE_TOKEN = "9aa7c48feee2cad4ca8ddeea673950b9"

# GeofenceAPI host
GEOFENCE_SERVER = "https://api.geofenceapi.org"
