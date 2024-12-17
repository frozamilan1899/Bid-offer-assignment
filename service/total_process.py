import random


def calculate_score(bid, base_price):
    """
    计算单个报价的得分
    """
    pr = abs(bid - base_price) / base_price  # 偏差率
    if bid > base_price:
        return max(0, 100 - pr * 100 * 2)  # 报价 > 基准价
    else:
        return max(0, 100 - pr * 100 * 1)  # 报价 <= 基准价

def generate_partner_bids(my_bid, num_partners=10, spread=1000):
    """
    生成围绕 my_bid 的随机报价，使报价更自然
    :param my_bid: 我的报价
    :param num_partners: 好伙伴的数量
    :param spread: 报价的上下浮动范围
    :return: 好伙伴的随机报价列表
    """
    partner_bids = []
    for _ in range(num_partners):
        # 随机生成一个在 [my_bid - spread, my_bid + spread] 范围内的报价
        random_bid = my_bid + random.randint(-spread, spread)
        # 确保报价满足 9000 <= bid <= 10000
        random_bid = max(9000, min(10000, random_bid))
        partner_bids.append(random_bid)
    
    return partner_bids


def simulate_bidding(my_bid, bad_bid_range=(9000, 10000)):
    """
    模拟所有玩家报价并验证结果
    :param my_bid: 我的报价
    :param bad_bid_range: 坏人报价范围
    :return: 好伙伴报价和对应得分
    """
    # 设计好伙伴的报价围绕我的报价对称分布且随机自然
    partner_bids = generate_partner_bids(my_bid)
    
    # 初始化成功标志
    success = False
    
    base_price = 0
    
    # 模拟坏人报价对得分的影响
    for bad_bid in range(bad_bid_range[0], bad_bid_range[1], 1):
        all_bids = partner_bids + [my_bid, bad_bid]
        
        # 去掉最高和最低报价
        remaining_bids = sorted(all_bids)[1:-1]
        
        # 计算基准价
        avg = sum(remaining_bids) / len(remaining_bids)
        k = random.choice([95, 96, 97, 98, 99, 100]) / 100  # 随机 k 值
        base_price = avg * k
        
        # 计算所有玩家的得分
        scores = [calculate_score(bid, base_price) for bid in all_bids]
        
        # 检查我的得分是否始终第一
        my_score = scores[all_bids.index(my_bid)]
        bad_score = scores[all_bids.index(bad_bid)]
        max_score = max(scores)
        
        if my_score < max_score:
            print(f"Failed: Bad guy or partner scored higher with bad_bid={bad_bid}!")
        else:
            success = True
            print(f"Succeed: My bid={my_bid}, score={my_score}")
            print(f"Succeed: Bad guy bid={bad_bid}, score={bad_score}")
            break
    
    # 如果模拟失败，返回空结果
    if not success:
        return [], [], success
    
    # 最终返回好伙伴报价及得分
    partner_scores = [calculate_score(bid, base_price) for bid in partner_bids]
    return partner_bids, partner_scores, success


# 设置我的报价
my_bid = 9900

# 模拟报价并输出结果
partner_bids, partner_scores, success = simulate_bidding(my_bid)

# 输出最终报价方案
if success and partner_bids:
    print("My Bid:", my_bid)
    print("Partner Bids and Scores:")
    for i, (bid, score) in enumerate(zip(partner_bids, partner_scores)):
        print(f"Partner {i + 1}: Bid = {bid}, Score = {score:.2f}")
else:
    print("Simulation failed to guarantee the highest score for my bid.")
