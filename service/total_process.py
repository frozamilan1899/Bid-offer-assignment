import random
from constant import BidFullMarks, K_Range
from utils import formula


bid_range=(9000, 10000)


def generate_partner_bids(my_bid, k, num_partners=10, spread=300):
    """
    生成围绕 my_bid 的随机报价，使报价更自然
    :param my_bid: 我的报价
    :param k: 随机系数
    :param num_partners: 好伙伴的数量
    :param spread: 报价的上下浮动范围
    :return: 好伙伴的随机报价列表
    """
    partner_bids = []
    while True:
        for _ in range(num_partners):
            # 随机生成一个在 [my_bid - spread, my_bid + spread] 范围内的报价
            # 生成一个以 10 为单位的随机数
            random_digit = random.randint(-spread // 10 + 1, spread // 10 - 1)
            if random_digit == 0: random_digit += 1
            random_increment = random_digit * 10
            # 计算最终的 bid
            random_bid = my_bid + random_increment
            # 确保报价在可控范围
            random_bid = max(bid_range[0], min(bid_range[1], random_bid))
            partner_bids.append(random_bid)
        # end for
        
        # 验证我的报价是否接近(接近率可以设置)各报价计算的基准价，但不大于
        tmp_base_price = formula.calculate_base_price(partner_bids + [my_bid], k)
        # print(f'tmp_base_price = {tmp_base_price}')
        if tmp_base_price < my_bid * (k/100.0):
            partner_bids.clear()
            continue # 重新算
        else:
            break
    # end while
    return partner_bids


def simulate_bidding(my_bid):
    """
    模拟所有玩家报价并验证结果
    :param my_bid: 我的报价
    :param bid_range: 坏人报价范围
    :return: 好伙伴报价和对应得分
    """
    # 随机 k 值
    k = random.choice(K_Range)
    # k = 100
    success = False
    base_price = 0
    # 好伙伴的报价列表
    partner_bids = generate_partner_bids(my_bid, k)
    
    print("My Bid:", my_bid)
    print(f"Partner Bids: {partner_bids}")
    
    success_rate = 0
    success_count = 0
    total_count = 0
    
    # 模拟坏人报价对得分的影响
    for bad_bid in range(bid_range[0], bid_range[1], 1):
        # partner_bids = generate_partner_bids(my_bid, k)
        
        if bad_bid < min(partner_bids + [my_bid]):
            continue
        if bad_bid > max(partner_bids + [my_bid]):
            continue
        
        total_count += 1
    
        all_bids = partner_bids + [my_bid, bad_bid]
        
        base_price = formula.calculate_base_price(all_bids, k)
        
        # 计算所有玩家的得分
        scores = [formula.calculate_bid_score(bid, base_price, BidFullMarks.TOTAL.value) for bid in all_bids]
        
        # 检查我的得分是否始终第一
        my_score = scores[all_bids.index(my_bid)]
        bad_score = scores[all_bids.index(bad_bid)]
        max_score = max(scores)
        
        if my_score < max_score:
            continue
            # print(f"Failed: Bad guy or partner scored higher with bad_bid={bad_bid}!")
        else:
            success = True
            success_count += 1
            print(f"Succeed: My bid={my_bid}, score={my_score}")
            print(f"Succeed: Bad guy bid={bad_bid}, score={bad_score}")
            # break
    # end for
    if success:
        success_rate = success_count / total_count
        print(f"success rate={success_rate*100}%")
    else:
        # 如果模拟失败，返回空结果
        return [], [], success, success_rate
    
    # 最终返回好伙伴报价及得分
    partner_scores = [formula.calculate_bid_score(bid, base_price, BidFullMarks.TOTAL.value) for bid in partner_bids]
    return partner_bids, partner_scores, success, success_rate


def main_fuc(my_bid):
    # 模拟报价并输出结果
    while True:
        partner_bids, partner_scores, success, success_rate = simulate_bidding(my_bid)
        # 输出最终报价方案
        if success and success_rate > 0.9999:
            print("My Bid:", my_bid)
            print("Partner Bids and Scores:")
            for i, (bid, score) in enumerate(zip(partner_bids, partner_scores)):
                print(f"Partner {i + 1}: Bid = {bid}, Score = {score:.2f}")
            # end for
            break
        else:
            print("Simulation failed to guarantee the highest score for my bid.")
    # end while



if __name__ == '__main__':
    print("start --->")
    
    # 设置我的报价
    my_bid = 9600
    main_fuc(my_bid)