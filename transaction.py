#Transaction class
class Transaction:    
    def __init__(self):
        self.date=''
        self.script_name=''
        self.buy_price=0.0
        self.sell_price=0.0
        self.quantity=0
        self.brokerage=0.0
        self.status=0
    
    def figures(self):
        print('***** '+self.script_name+' *****')
        print('Date: ',self.date)
        if self.status!=0:
            print('Type: Delivery')
            if self.status<0:
                print('-%d @ %f'%(self.quantity,self.sell_price))
            else:
                print('+%d @ %f'%(self.quantity,self.buy_price))
            print('Brokerage: ',self.brokerage)
            print('Gain or cost: ',self.get_gain_or_cost())
        else:
            print('Type: Intraday')
            print('+%d @ %f | -%d @ %f'%(self.quantity,self.buy_price,self.quantity, self.sell_price))
            print('Brokerage: ',self.brokerage)
            print('P&L: ',self.get_pl())

    def get_pl_with_brokerage(self):
        if self.status!=0:
            return 0
        else:
            return round(((self.quantity*self.sell_price)-(self.quantity*self.buy_price))-self.brokerage,2)

    def get_pl(self):
        if self.status!=0:
            return 0
        else:
            return (self.quantity*self.sell_price)-(self.quantity*self.buy_price)
    
    def get_gain_or_cost(self):
        if self.status==-1:
            return -1*(self.quantity*self.sell_price)
        elif self.status==1:
            return self.quantity*self.sell_price
        else:
            return 0