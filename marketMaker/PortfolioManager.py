class PortfolioManager:
    def __init__(self):
        self.syms = set(['ETH','BTC','USD','BNB'])
        self.positions = {}
        self.locked = {}

    def getPosition(self, sym):
        return self.positions.get(sym, 0.0)


    def processPositionUpdate(self, msg):
        for pu in msg['B']:
            self.positions[pu['a']] = float(pu['f']) + float(pu['l'])
            self.locked[pu['a']] = float(pu['l'])
        return




