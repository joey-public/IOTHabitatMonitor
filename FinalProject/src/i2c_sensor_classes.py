class I2CDevice:
    def __init__(self, i2c_lib, sda_pin, scl_pin, addr, data_bytes):
        self.i2c_lib = i2c_lib
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        self.addr = addr
        self.data_bytes = data_bytes
        self.raw_data = bytearray(self.data_bytes)

    #reads once from the device and then returns the results
    def read_and_get_data(self):
        device = self._open_pynq_device_i2c_bus()
        self.i2c_lib.i2c_read(device, self.addr, self.raw_data, self.data_bytes)
        self.i2c_lib.i2c_close(device)
        return self.raw_data
    
    #reads data from the device in a loop
    #intended to be run on its own thread or process  
    #count = -1 will run forever
    def read_data_loop(self, delay_func, shared_data_queue, count=-1):
        device = self._open_pynq_device_i2c_bus()
        i = 0
        while(i<count):
            self.i2c_lib.i2c_read(device, self.addr, self.raw_data, self.data_bytes)
            shared_data_queue.put(self.raw_data)
            if count != -1: i+=1
            delay_func(delay)
        self.i2c_lib.i2c_close(device)
    #internal/private function to open the i2c bus
    def _open_pynq_device_i2c_bus(self):
        device = self.i2c_lib.i2c_open(self.sda_pin, self.scl_pin)
        self.i2c_lib.i2c_write(device, self.addr, self.raw_data, 1)
        return device
    
class Ky015Sensor(I2CDevice):
    def __init__(self, i2c_lib, sda_pin, scl_pin, addr):
        super().__init__( i2c_lib, sda_pin, scl_pin, addr, 5)
        self.temperature = None
        self.humidity = None

    def decode_raw_data(self, data):
        temp = data[2] + data[3]/100
        hum = data[0] + data[1]/100
        return temp, hum

    def get_temp_and_hum_data(self):
        raw_data = self.read_and_get_data()
        t, h = self.decode_raw_data(raw_data)
        self.temperature = t
        self.humidity = h
        return t, h    
