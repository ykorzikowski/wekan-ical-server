from wekanapi import WekanApi
from http.server import BaseHTTPRequestHandler, HTTPServer
import vobject
import dateutil.parser
import os
import logging as log

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 80

WEKAN_HOST = os.getenv('WEKAN_HOST', 'http://127.0.0.1:8090')
WEKAN_USER = os.getenv('WEKAN_USER', 'admin')
WEKAN_PASSWORD = os.getenv('WEKAN_PW', 'admin')

def create_ical_event(cal, board, card, card_info):
    event = cal.add('vevent')
    event.add('summary').value = board.title + ": " + card_info['title']
    event.add('dtstart').value = dateutil.parser.parse(card_info['dueAt'])
    if 'description' in card_info: event.add('description').value = card_info['description']
    event.add('url').value = WEKAN_HOST + "/b/" + board.id + "/x/" + card.id

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/calendar")
        self.end_headers()

    def do_GET(self):
        log.info("new http request")
        self.respond({'status': 200})

    def handle_http(self, status_code, path):
        log.debug("api connecting...")
        wekan_api = WekanApi(WEKAN_HOST, {"username": WEKAN_USER, "password": WEKAN_PASSWORD})
        log.debug("api connected")

        cal = vobject.iCalendar()
        boards = wekan_api.get_user_boards()
        for board in boards:
            log.info("collecting board {}")
            cardslists = board.get_cardslists()
            for cardslist in cardslists:
                log.debug("collecting cardlist")
                cards = cardslist.get_cards()
                for card in cards:
                    log.debug("collecting card")
                    info = card.get_card_info()
                    if "dueAt" in info: create_ical_event(cal, board, card, info)

        log.info("finished collection")
        log.debug(cal.serialize())
        return bytes(cal.serialize(), 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    log.basicConfig(level=log.DEBUG)
    server_class = HTTPServer
    httpd = server_class((LISTEN_HOST, LISTEN_PORT), MyHandler)
    try:
        log.info("starting http server")
        httpd.serve_forever()
    finally:
        httpd.server_close()
