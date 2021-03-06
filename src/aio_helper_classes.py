from Adafruit_IO import Client, Feed, Group
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
        self.lbtFeed = self.feeds('low-brightness-threshold')
        self.hbtFeed = self.feeds('high-brightness-threshold')
        self.lttFeed = self.feeds('low-temperature-threshold')
        self.httFeed = self.feeds('high-temperature-threshold')
        self.lhtFeed = self.feeds('low-humidity-threshold')
        self.hhtFeed = self.feeds('high-humidity-threshold')
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
        client_count = len(client_ids)
        for num, cid in enumerate(client_ids):
            if self.client_id == cid.value:
                self.client_number = client_count - num 
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


class HabitatMonitorServer(Client):
    def __init__(self, aio_uname, aio_key, server_id):
        super().__init__(aio_uname, aio_key)
        print('Creating Habitat Mon Server...')
        self.server_id = server_id
        self.client_ids = self.get_client_ids()
        self.high_bright_feed = self.feeds('high-brightness-threshold')
        self.high_hum_feed= self.feeds('high-humidity-threshold')
        self.high_temp_feed = self.feeds('high-temperature-threshold')
        self.low_bright_feed = self.feeds('low-brightness-threshold')
        self.low_hum_feed = self.feeds('low-humidity-threshold')
        self.low_temp_feed = self.feeds('low-temperature-threshold')
        self.temperature_group = self.groups('temperature-measurements')
        self.humidity_group = self.groups('humidity-measurements')
        self.brightness_group = self.groups('brightness-measurements')
        self.client_status_feed = self.feeds('client-status')
        self.high_temp, self.low_temp = None, None
        self.high_hum, self.low_hum = None, None
        self.high_bright, self.low_bright = None, None
        self.LOWER_THEN_THRESHOLD = 'READING BELOW THRESHOLD'
        self.HIGHER_THEN_THRESHOLD = 'READING ABOVE THRESHOLD'
    def get_client_ids(self):
        client_id_list = []
        id_feed = self.feeds('client-ids')
        cids = self.data(id_feed.key)
        for client_id in cids:
            client_id_list.append(client_id.value)
        return client_id_list
    def get_client_num(self,client_feed_key):
        return int(client_feed_key[-1])
    
    @property
    def high_temp(self):
        return self.__high_temp
    @high_temp.setter
    def high_temp(self, val):
        if val != None:
            self.send(self.high_temp_feed.key, val)
        self.__high_temp = val
    @property
    def high_hum(self):
        return self.__high_hum
    @high_hum.setter
    def high_hum(self, val):
        if val != None:
            self.send(self.high_hum_feed.key, val)
        self.__high_hum = val
    @property
    def high_bright(self):
        return self.__high_bright
    @high_bright.setter
    def high_bright(self, val):
        if val != None:
            self.send(self.high_bright_feed.key, val)
        self.__high_bright = val
    @property
    def low_temp(self):
        return self.__low_temp
    @low_temp.setter
    def low_temp(self, val):
        if val != None:
            self.send(self.low_temp_feed.key, val)
        self.__low_temp = val
    @property
    def low_hum(self):
        return self.__low_hum
    @low_hum.setter
    def low_hum(self, val):
        if val != None:
            self.send(self.low_hum_feed.key, val)
        self.__low_hum = val
    @property
    def low_bright(self):
        return self.__low_bright
    @low_bright.setter
    def low_bright(self, val):
        if val != None:
            self.send(self.low_bright_feed.key, val)
        self.__low_bright = val       
