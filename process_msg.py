from transaction import Transaction

def split_order(entity):
    if '+' in entity:
        q_p_lst=entity.split('@')
        quan=q_p_lst[0]
        quan=int(quan.replace('+',''))
        price=float(q_p_lst[1])
        return {'type':'B',
                 'price': price,
                 'quantity': quan }
    else:
        q_p_lst=entity.split('@')
        quan=q_p_lst[0]
        quan=int(quan.replace('-',''))
        price=float(q_p_lst[1])
        return {'type':'S',
                 'price': price,
                 'quantity': quan }

def first_entry(order,trans_lst):
    if order['type'] == 'B':
        trans_lst[-1].buy_price=order['price']
        trans_lst[-1].quantity=order['quantity']
        trans_lst[-1].status= trans_lst[-1].status+1
    else:
        trans_lst[-1].sell_price=order['price']
        trans_lst[-1].quantity=order['quantity']     
        trans_lst[-1].status= trans_lst[-1].status-1

def second_entry(order,trans_lst):
    if order['quantity']==trans_lst[-1].quantity:
        first_entry(order,trans_lst)
    else:
        mix_quan=int(order['quantity']-trans_lst[-1].quantity)
        if mix_quan>0:
            first_order={'type':'S',
                 'price': order['price'],
                 'quantity':trans_lst[-1].quantity}
            first_entry(first_order,trans_lst)
            #handle second order
            second_order={'type':order['type'],
                    'price': order['price'],
                    'quantity':abs(order['quantity']-trans_lst[-1].quantity)}
        else:
            trans_lst[-1].quantity=trans_lst[-1].quantity-abs(mix_quan)
            first_order={'type':order['type'],
                 'price': order['price'],
                 'quantity':trans_lst[-1].quantity}
            first_entry(first_order,trans_lst)
            second_order={'type':'B',
                    'price': trans_lst[-1].buy_price,
                    'quantity':abs(mix_quan)}

        t_tans= Transaction()
        t_tans.script_name=trans_lst[-1].script_name
        trans_lst.append(t_tans)
        first_entry(second_order,trans_lst)

def get_outcome(amt_w):
    amt_w=amt_w.strip()
    if 'Dr' in amt_w:
        amt=amt_w[0:-2]
        amt=-1*float(amt)
    else:
       amt=amt_w[0:-2]
       amt= float(amt)
    
    return amt

def find_brokage(amt,trans_lst):
    d_amt=0
    i_amt=0
    count=0

    for i in range(0,len(trans_lst)):
        if trans_lst[i].status==0:
            pl=trans_lst[i].get_pl()
            i_amt=i_amt+pl
            count=count+1
        else:
            if trans_lst[i].status<0:
                gain=trans_lst[i].quantity*trans_lst[i].sell_price
                d_amt=d_amt+gain
            else:
                cost=trans_lst[i].quantity*trans_lst[i].buy_price
                d_amt=d_amt-cost
            count=count+1
    brokerage=(amt-i_amt)-d_amt
    brokerage=-1*brokerage
    return brokerage,count

#Funtion to add brokerage to transactions
def add_brokerage_date(brokerage,count,date,trans_lst):
    brok_per=brokerage//count
    for t in trans_lst:
        t.brokerage=brok_per
        t.date=date

#Main Function
def get_transactions(msg):
    msg=msg.strip()
    indx=msg.find('Bill')
    #Getting amout Dr/Cr and Date
    amt_indx=msg.find('Amt:Rs.')
    date=msg[7:17]
    amt_indx=amt_indx+7

    l=len(msg)
    amt_w=msg[amt_indx:l]
    amt = get_outcome(amt_w)
    #trimming msg getting ride of all unwanted text
    trim_msg=msg[30:indx-1]
    entity_lst=trim_msg.split(' ')
    #
    trans_lst=[]
    for i in range(0,len(entity_lst)):
        if '+' not in entity_lst[i] and '-' not in entity_lst[i]:
            temp_tran= Transaction()
            temp_tran.script_name=entity_lst[i]
            trans_lst.append(temp_tran)
        else:
            order=split_order(entity_lst[i])
            if trans_lst[-1].status==0:
                first_entry(order,trans_lst)
            else:
                second_entry(order,trans_lst)
    #Finding Intarday Amt
    brokerage,count=find_brokage(amt,trans_lst)

    add_brokerage_date(brokerage,count,date,trans_lst)           
    return amt,trans_lst


