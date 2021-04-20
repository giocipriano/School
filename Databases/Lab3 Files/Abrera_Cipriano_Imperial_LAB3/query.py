from decimal import Decimal
import user_ops as user
import order_ops as order_ops
from pprint import pprint

if __name__ == '__main__':
    pprint('       ALL PENDING ORDERS      ')
    pprint('-------------------------------')
    pprint(order_ops.query_allpending())
    pprint('      ALL SHIPPING ORDERS      ')
    pprint('-------------------------------')
    pprint(order_ops.query_allshipping())