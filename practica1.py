#!/usr/bin/python3

import webapp
import csv


class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    content = {}
    content2 = {}

    def read(self):
        try:
            with open("data.csv") as csfile:
                entry = csv.reader(csfile)
                for row in entry:
                    value1 = int(row[0])    # Number
                    value2 = row[1]         # URL
                    self.content[value1] = value2
                    self.content2[value2] = value1
        except FileNotFoundError:
            print("No file found")

    def write(self):
        with open("data.csv", "w") as csvfile:
            wr = csv.writer(csvfile)
            for elem in self.content:
                wr.writerow([elem, self.content[elem]])

    def parse(self, request):
        """Return the resource name (including /)"""
        self.read()
        return (request.split(' ', 1)[0],
                request.split(' ', 2)[1],
                request.split('\r\n\r\n')[-1])

    def process(self, parsed):
        """Process the relevant elements of the request.
        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        method, resourceName, body = parsed
        if (resourceName=="/"):
            if (method=="GET"):
                httpCode="200 OK"
                htmlBody=("<html><body><form method= 'POST' action=''>" +
                            "<input type = 'text' name= 'url'>" +
                            "<input type= 'submit' value='Enviar'></form>" +
                            "<p>" + str(self.content) + "</p></html>")
            elif (method=="POST"):
                import urllib.parse
                url = urllib.parse.unquote(body)
                if ("=" in body):   #compruebo QS
                    url = url.split('=')[-1]
                    if url.startswith("http://") or url.startswith("https://"):
                        print("Found http://")
                    else:
                        url="http://" + url
                    # //
                    if (url in self.content2):
                        httpCode = "404 Not Found"
                        htmlBody = ("<html><body>Already saved in:" +
                                    "http://localhost:1234/" +
                                    str(self.content2[url]) + "</body></html>")
                    else:
                        self.content[len(self.content)] = url
                        self.content2[url] = len(self.content2)
                        self.write()
                        httpCode="200 OK"
                        htmlBody=("<html><body><p><a href = " +
                                    self.content[(len(self.content) - 1)] +
                                    ">" +
                                    self.content[(len(self.content) - 1)] +
                                    "</a></p><p><a href = " +
                                    self.content[(len(self.content) - 1)] +
                                    ">" + 'http://localhost:1234/' +
                                    str(len(self.content) - 1) +
                                    "</a></p></body></html>")
                else:
                    httpCode="400 Bad Request"
                    htmlBody=("<html><body>POST without body</html>")
            else:
                httpCode="405 Method Not Allowed"
                htmlBody=("<html><body>Operation not allowed" +
                            "</html>")
        else:
            resourceName=resourceName.split("/")[-1]
            if (resourceName=="favicon.ico"):
                httpCode="404 Not Found"
                htmlBody=("<html><body>Found favicon</html>")
                recvSocket.close()
            elif (int(resourceName) in self.content):
                resourceName=int(resourceName)
                httpCode="301 Moved Permanently"
                htmlBody=("<html><meta http-equiv= 'Refresh'" +
                            "content =5;url=" + self.content[resourceName] +
                            "><body><h1>Hello</h1></body></html>" +
                            "\r\n" +
                            "<html><body><p> Redirecting " +
                            "to the site... " + self.content[resourceName] +
                            "</p></body></html>")
            else:
                httpCode="404 Not Found"
                htmlBody=("<html><body>404 Not Found</html>")
        return (httpCode, htmlBody)
        
if __name__ == "__main__":
    testWebApp=contentApp("localhost", 1234)
