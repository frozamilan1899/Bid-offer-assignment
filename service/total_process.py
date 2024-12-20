import numpy as np
import random
from service.constant import BidFullMarks, K_Range, MAX_TOTAL_BID, MAX_TOTAL_BID_limit_range
from service import formula

bid_range=(MAX_TOTAL_BID*MAX_TOTAL_BID_limit_range[0], MAX_TOTAL_BID*MAX_TOTAL_BID_limit_range[1])
partner_bid_spread=300
all_bids_range = np.arange(bid_range[0], bid_range[1], 1)

def generate_partner_bids(my_bid, k, num_partners=10):
    """
    生成围绕 my_bid 的随机报价，使报价更自然，报价浮动范围在 partner_bid_spread 之内
    :param my_bid: 我的报价
    :param k: 随机系数
    :param num_partners: 好伙伴的数量
    :return: 好伙伴的随机报价列表
    """
    partner_bids = []
    while True:
        partner_bids.clear()    # 清空之前的报价，避免重复
        for _ in range(num_partners):
            # 生成一个以 10 为单位的随机数
            random_digit = random.randint(-partner_bid_spread // 10 + 1, partner_bid_spread // 10 - 1)
            # 防止生成和我的报价相同的报价
            if random_digit == 0: random_digit += 1
            random_increment = random_digit * 10
            # 计算最终的 bid
            random_bid = my_bid + random_increment
            # 确保报价在可控范围
            random_bid = max(bid_range[0], min(bid_range[1], random_bid))
            partner_bids.append(random_bid)
        # end for
        
        # 验证我的报价是否接近各报价计算的基准价，但不大于
        tmp_base_price = formula.calculate_base_price(partner_bids + [my_bid], k)
        # print(f'tmp_base_price = {tmp_base_price}')
        if tmp_base_price < my_bid * (k/100.0):
            continue # 重新算
        else:
            break
    # end while
    return partner_bids


def simulate_bidding(my_bid, k):
    """
    模拟所有玩家报价并验证结果
    :param my_bid: 我的报价
    :param bid_range: 坏人报价范围
    :return: 好伙伴报价和对应得分
    """
    # 好伙伴的报价列表
    partner_bids = generate_partner_bids(my_bid, k)
    print("My Bid:", my_bid)
    print(f"Partner Bids: {partner_bids}")
    
    base_price = 0
    success_count = 0
    total_count = 0
    
    # 模拟坏人报价对得分的影响
    for bad_bid in all_bids_range:
        # 坏人报价在报价列表范围以外的话，得分肯定低，可以不用你考虑
        if bad_bid < min(partner_bids + [my_bid]) or bad_bid > max(partner_bids + [my_bid]):
            continue
        
        # 坏人报价参与基准价计算并计算得分时，我们算一次参与过程
        total_count += 1
    
        # 计算基准价
        all_bids = partner_bids + [my_bid, bad_bid]
        base_price = formula.calculate_base_price(all_bids, k)
        
        # 计算所有玩家的得分
        scores = [formula.calculate_total_bid_score(bid, base_price, BidFullMarks.TOTAL.value) for bid in all_bids]
        
        # 检查我的得分是否始终第一
        my_score = scores[all_bids.index(my_bid)]
        # bad_score = scores[all_bids.index(bad_bid)]
        
        # 如果我的分数就是最大分数，那么算一次成功
        if my_score == max(scores):
            success_count += 1
            # print(f"Succeed: My bid={my_bid}, score={my_score}")
            # print(f"Succeed: Bad guy bid={bad_bid}, score={bad_score}")
        # 不退出循环
    # end for
    
    # 计算成功率
    success_rate = (success_count / total_count) * 100
    print(f"Success rate={success_rate:.2f}%")

    return partner_bids, base_price, success_rate


def main_func(my_bid, k):
    final_bids_scores = []
    
    # 模拟报价并输出结果
    try_limit = 2000
    try_times = 1
    while True:
        # 超过尝试上限就不算了
        if try_times > try_limit:
            break
        
        print(f'-->My Bid:{my_bid}, K:{k}, try times={try_times}')
        partner_bids, base_price, success_rate = simulate_bidding(my_bid, k)
        
        # 如果我的报价比所有的伙伴报价都小，重算
        if my_bid < min(partner_bids):
            try_times += 1
            continue
        
        # 输出最终报价方案
        if success_rate > 99.99:
            print("Bingo!===================================")
            print(f"Base price={base_price}")
            # 计算包括我在内的所有报价得分
            bids = partner_bids + [my_bid]
            scores = [formula.calculate_total_bid_score(bid, base_price, BidFullMarks.TOTAL.value) for bid in bids]
            # 将bids和scores组合，并按照scores从高到低排序
            sorted_bids_scores = sorted(zip(bids, scores), key=lambda x: x[1], reverse=True)
            # 排序和打印最终报价和得分
            for i, (bid, score) in enumerate(sorted_bids_scores):
                bid_label = f"SelfBid {i + 1}" if bid == my_bid else f"Partner {i + 1}"
                print(f"{bid_label}: Bid = {bid}, Score = {score:.2f}")
            # 跳出
            final_bids_scores = sorted_bids_scores
            break
        else:
            print("Simulation failed to guarantee the highest score for my bid.")
            try_times += 1
            
    # end while
    return final_bids_scores



if __name__ == '__main__':
    print("start --->")
    
    # 设置我的报价
    my_bid = 9600
    # 随机 k 值
    k = random.choice(K_Range)
    main_func(my_bid, k)
    