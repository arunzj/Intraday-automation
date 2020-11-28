import process_msg
import sheet
from datetime import datetime

if __name__ == "__main__":

    msg_file=open('messages.txt')
    for msg in msg_file:
        amt,trans_lst=process_msg.get_transactions(msg)
        print("Saving Tansactions for :",trans_lst[0].date)
        intra_worksheet=sheet.get_worksheet('IntradayTrades')
        intra_records=intra_worksheet.get_all_records()
        intra_next_row=str(len(intra_records)+2)
        del_worksheet=sheet.get_worksheet('SwingTrades')
        del_records=del_worksheet.get_all_records()
        del_next_row=len(del_records)+2
        t_date=trans_lst[0].date

        total_pl=0
        intra_count=0
        del_count=0
        for t in trans_lst:
            if t.status==0:
                total_pl = total_pl + t.get_pl_with_brokerage()
                intra_count=intra_count+1
            else:
                del_count=del_count+1
                #if a new Delivery Buy Order
                if t.status>0:
                    del_worksheet.update('A'+str(del_next_row),t_date)
                    del_worksheet.update('B'+str(del_next_row),'Open')
                    del_worksheet.update('C'+str(del_next_row),'Upx')
                    del_worksheet.update('D'+str(del_next_row),t.script_name)
                    del_worksheet.update('E'+str(del_next_row),t.quantity)
                    del_worksheet.update('F'+str(del_next_row),t.buy_price)
                    del_worksheet.update('H'+str(del_next_row),t.brokerage)
                    del_next_row=del_next_row+1
                else:
                    found_match='N'
                    r_poniter=len(del_records)-1
                    for i in range(r_poniter-3,r_poniter+1):
                        if del_records[i]['Status']=='Open' and del_records[i]['Script Name']==t.script_name and int(del_records[i]['Quantity'])==t.quantity:
                            u_row=i+2
                            found_match='Y'
                            del_worksheet.update('B'+str(u_row),'Closed')
                            del_worksheet.update('G'+str(u_row),t.sell_price)
                            charges=int(del_records[i]['Charges'])+t.brokerage
                            del_worksheet.update('H'+str(u_row),charges)
                    if found_match=='N':
                        print('Couldt FInd Match For Delivery***')


        if intra_count>0:
            intra_worksheet.update('A'+intra_next_row,t_date)
            intra_worksheet.update('B'+intra_next_row,'Upx')
            intra_worksheet.update('C'+intra_next_row,'INTRADAY')
            intra_worksheet.update('D'+intra_next_row,total_pl)

        
