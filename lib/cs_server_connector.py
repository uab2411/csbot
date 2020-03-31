import a2s


class CS_Server_Connector():

    def __init__(self, serverip):
        self.server_ip = serverip[0]
        self.server_port = serverip[1]
        self.address = (self.server_ip, self.server_port)

    def get_game_info(self):
        info = a2s.info(self.address)
        # players=a2s.players(self.address)
        serv_details = {'serv_name': info.server_name, 'map': info.map_name, 'player_count': info.player_count,
                        'max_players': info.max_players, 'bot_count': info.bot_count, 'ping': info.ping}
        return serv_details
