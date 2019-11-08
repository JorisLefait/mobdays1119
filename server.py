import http.server
import requests
import json
 
PORT = 8888
server_address = ("", PORT)

class myHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/coucou" : 
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes('Coucou toi meme', 'utf-8'))
            return
        elif self.path == "/daystate" : 
            r = requests.get("http://192.168.2.54/api/embedded_light/state?embedded_light_api_key=ppDk0rATHKv8vyqlzjvVnNIYc")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            d = r.content
            self.wfile.write(d)
            return
        elif self.path == "/motion_sensor" :
            data = self.rfile.read(int(self.headers["Content-Length"]))
            obj = json.loads(data.decode('utf-8'))
            print (self.path)
            try :
                if obj['motion detected'] :
                    print ('test')
                    r = requests.get("http://192.168.1.77/api/embedded_light/state?embedded_light_api_key=ppDk0rATHKv8vyqlzjvVnNIYc")
                    self.send_response(200)
                    self.end_headers()
                    data = r.json()
                    if data["state_str"] == "Nuit" :
                        print ('nuit')
                        requests.post("http://192.168.1.35/api/led_rgb", data = {"embedded_led_rgb_api_key" : "iYCFjYE4tTnpiJJ6psf4axjTN", "red" : 1, "green" : 1, "blue": 1}) 
                    elif data["state_str"] == "Jour" :
                        print ('Jour')
                        requests.post("http://192.168.1.35/api/led_rgb", data = {"embedded_led_rgb_api_key" : "iYCFjYE4tTnpiJJ6psf4axjTN", "red" : 0, "green" : 0, "blue": 0}) 
                    return
                else: 
                    requests.post("http://192.168.1.35/api/led_rgb", data = {"embedded_led_rgb_api_key" : "iYCFjYE4tTnpiJJ6psf4axjTN", "red" : 0, "green" : 0, "blue": 0}) 
                    self.send_response(200)
                    self.end_headers()
                    return
            except : 
                self.send_response(200)
                self.end_headers()
                return  
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(self.path[1:], 'utf-8'))
            return

server = http.server.HTTPServer
handler = myHandler
handler.cgi_directories = ["/"]
print("Serveur actif sur le port :", PORT)

httpd = server(server_address, handler)
httpd.serve_forever()