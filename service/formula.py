

def calculate_total_bid_score(bid, base_price, full_marks):
    """
    计算总报价的得分
    """
    deviation_rate = calculate_deviation_rate(bid, base_price)
    if bid > base_price:
        return max(0, full_marks - deviation_rate * 100 * 2)  # 报价 > 基准价
    else:
        return max(0, full_marks - deviation_rate * 100 * 1)  # 报价 <= 基准价
    
def calculate_inventory_bid_score(bid, base_price, full_marks):
    """
    计算清单报价的得分
    """
    deviation_rate = calculate_deviation_rate(bid, base_price)
    if bid > base_price:
        return max(0, full_marks - deviation_rate * 100 * 0.05)  # 报价 > 基准价
    else:
        return max(0, full_marks - deviation_rate * 100 * 0.02)  # 报价 <= 基准价
    
def calculate_measure_bid_score(bid, base_price, full_marks):
    """
    计算措施报价的得分
    """
    deviation_rate = calculate_deviation_rate(bid, base_price)
    if bid > base_price:
        return max(0, full_marks - deviation_rate * 100 * 0.1)  # 报价 > 基准价
    else:
        return max(0, full_marks - deviation_rate * 100 * 0.1)  # 报价 <= 基准价
    

def calculate_deviation_rate(bid, base_price):
    """
    偏差率
    """
    deviation_rate = abs(bid - base_price) / base_price
    return deviation_rate


def calculate_base_price(all_bids, k_or_r):
    """
        计算所有报价的基准价
    """
    # 去掉最高和最低报价
    sorted_bids = sorted(all_bids)
    trimmed_bids = sorted_bids[1:-1]
    # 计算基准价
    avg = sum(trimmed_bids) / len(trimmed_bids)
    base_price = avg * (k_or_r / 100)
    return base_price


if __name__ == '__main__':
    print("test --->")
    ret = calculate_total_bid_score(9900, 9544, 100)
    print(f'score = {ret}')