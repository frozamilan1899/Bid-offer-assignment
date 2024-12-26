from enum import Enum

class BidFullMarks(Enum):
    TOTAL = 35
    INVENTORY = 50
    MEASURE = 15
    
K_Range = [95, 96, 97, 98, 99, 100]
R_Range = [90, 91, 92, 93, 94, 95, 96, 97]

# 总投标最高限价
MAX_TOTAL_BID = 10000
# 总投标报价范围
MAX_TOTAL_BID_limit_range = (0.92, 1.00)

# 清单投标最高限价
MAX_INVENTORY_BID = 8000
# 清单标报价范围
MAX_INVENTORY_BID_limit_range = (0.70, 1.10)

# 措施投标最高限价
MAX_MEASURE_BID = 2000
# 措施投标报价范围
MAX_MEASURE_BID_limit_range = (0.50, 1.20)

BID_SUCCESS_RATE = 99.99

