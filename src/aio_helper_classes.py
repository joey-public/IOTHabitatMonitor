from Adafruit_IO import Client, Feed
class HabitatMonitorClient(Client):
    def __init__(self, aio_uname, aio_key, client_id):
        print('creating new HabitatMonitor...')
        super().__init__(aio_uname, aio_key)
        self.CLIENT_ID_FEED = 'client-ids'
        self.FEED_GROUPS = {
            'temperature':'temperature-measurements',  
            'humidity':'humidity-measurements', 
            'brightness':'brightness-measurements' 
        }
        self.client_id = client_id
        self.temperature_feed = None
        self.humidity_feed = None
        self.brightness_feed = None
        self.client_number = None
        self._initilize_feeds()
        print('HabitatMonitorClientsetup')

    #private methods
    def _initilize_feeds(self):
        if not(self._is_new_client()):
            client_id_feed = self.feeds(self.CLIENT_ID_FEED)
            self.client_number = len(self.data(client_id_feed.key))
        else:
            self._create_new_feeds()
        self._set_feeds()

    def _set_feeds(self):
        self.temperature_feed = self.feeds('temperature-measurements.temperature-{}-{}'.format(self.client_id, self.client_number))
        self.humidity_feed = self.feeds('humidity-measurements.humidity-{}-{}'.format(self.client_id, self.client_number))
        self.brightness_feed = self.feeds('brightness-measurements.brightness-{}-{}'.format(self.client_id, self.client_number))

    def _is_new_client(self):
        client_ids_feed = self.feeds(self.CLIENT_ID_FEED)
        client_ids = self.data(client_ids_feed.key)
        for cid in client_ids:
            if self.client_id == cid.value:
                return False
        return True

    def _can_create_feeds(self):
        #TODO send request to add a new client to the cloud
        #the server board can recevie the request and 
        #decide if the board with this client_id is allowed to join
        return True #for now always return True

    def _create_new_feeds(self):
        if not(self._can_create_feeds()):
            return 
        client_id_feed = self.feeds(self.CLIENT_ID_FEED)
        cur_client_count = len(self.data(client_id_feed.key))
        self.client_number = cur_client_count + 1
        self.send(client_id_feed.key, self.client_id)
        for feed_name, group_name in self.FEED_GROUPS.items():
            feed = Feed(name='{}-{}-{}'.format(feed_name, self.client_id, self.client_number,))
            self.create_feed(feed, group_name)
