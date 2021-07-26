import time, urequests

class api:
    def __init__(self) -> None:
        self._email_url = "https://maker.ifttt.com/trigger/email/with/key/CS5bYnTkWNS01hQSP5rYU"
        self._graph_url = "https://api.thingspeak.com/update?api_key=623UWTQMR6ZMQPH4"
        self._email_time = time.time()
        self._graph_time = time.time()
    
    def send_email(self, temp: float) -> None:
        if (time.ticks_diff(time.time(), self._email_time) > 60):
            endpoint = self._email_url + "?value1=" + "{:.2f}°C"
            response = urequests.get(endpoint)
            print("Send email")
            print("Response:", response.text)
            print ("Status:", response.status_code)
            response.close()
            self._email_time = time.time()

    def graph_temp(self, temp: float) -> None:
        if (time.ticks_diff(time.time(), self._graph_time) > 15):
            endpoint = self._graph_url + "&field1=" + str(temp)
            response = urequests.get(endpoint)
            print("Graph")
            print("Response", response.text)
            print ("Status", response.status_code)
            response.close()
            self._graph_time = time.time()
