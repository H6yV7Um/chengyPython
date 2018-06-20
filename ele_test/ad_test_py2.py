# -*- coding: utf-8 -*-
import requests
import json
import time

post_data = '{"iface":"com.eleme.search.rank.face.RankService","method":"searchRestaurantRank",' \
            '"args":{"bizRequest":"{\\"desc\\":false,\\"deviceId\\":\\"450E93C6-6650-4D17-9FAF-1C338F9935DE\\",' \
            '\\"limit\\":100,\\"fromPage\\":\\"home\\",\\"searchQuery\\":\\"{}\\",\\"reviewMode\\":true,\\"os\\":\\"iOS/11.1.2\\",' \
            '\\"brandFolding\\":false,\\"sortBy\\":\\"INTELLIGENCE\\",\\"cityId\\":\\"1\\",\\"offset\\":0,\\"uid\\":\\"15926226\\",' \
            '\\"longitude\\":0,\\"debug\\":0,\\"kaTop\\":false,\\"network\\":\\"WIFI\\",\\"area\\":{\\"districtId\\":5255,' \
            '\\"provinceId\\":10009,\\"cityId\\":1},\\"newUser\\":false,\\"weather\\":\\"CLEAR_DAY\\",\\"filterAttributes\\":{},' \
            '\\"networkOperator\\":\\"46000\\",\\"lbs\\":\\"POINT(116.481048584 39.9967956543)\\",' \
            '\\"reviewTime\\":\\"2017-12-30T12:30:00\\"}"}} '


def getRankList(point):
    request_data = post_data.replace("116.481048584 39.9967956543", point)
    json_data = json.loads(request_data)
    url = 'http://localhost:8859/rpc'
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=json_data, headers=headers)
    # print(r.text)
    # print(r.encoding)
    response_json = json.loads(r.text)
    result_str = response_json['result']
    result_json = json.loads(result_str)
    rankList = result_json['rankList']
    try:
        ad_list = result_json['reviewInfo']['adResponse']['shopScores']
    except Exception as err:
        print(err)
        ad_list = []
    return rankList, ad_list


def checkAdOrder(fullList, subList):
    orderList = []
    for id in subList:
        orderList.append(fullList.index(id))
    if len(subList) == 0:
        return True
    preIndex = orderList[0]
    for index in orderList[1:]:
        if index < preIndex:
            return False
        else:
            preIndex = index
    return True


def checkAdNums(rankListNum, ad_count):
    ad_index_list = [3, 4, 9, 11, 14, 17, 19, 24]
    # 假设数据满足 所有动态广告位都填充
    if rankListNum >= 24:
        return ad_count == 8
    for i, nums in enumerate(ad_index_list):
        if rankListNum < nums:
            return ad_count == i


def checkAdInsertion(point="121.3827466965 31.2328393274"):
    rankList, adList = getRankList(point)
    ad_count = 0
    index_list = []
    ad_id_list = []
    for r in rankList:
        if r['reasonType'] == 'A':
            ad_count = ad_count + 1
            index_list.append(r['index'])
            ad_id_list.append(r['id'])
    full_ad_ids = []
    for ad in adList:
        full_ad_ids.append(ad['shopId'])

    print "rank_list=======>" + str(len(rankList))
    print "ad_count========>" + str(ad_count)
    print "ad_index========>" + str(index_list)
    ad_num_check = checkAdNums(len(rankList), ad_count)
    ad_order_check = checkAdOrder(full_ad_ids, ad_id_list)
    print "check_ad_count======>" + str(ad_num_check)
    print "check_ad_order======>" + str(ad_order_check)
    return ad_num_check and ad_order_check


def generatePoint():
    point_list = []
    base_latitude = 31.170
    base_longitude = 121.370
    for x in list(range(16)):
        for y in list(range(101)):
            point = str(base_longitude + x * 0.01) + " " + str(base_latitude + y * 0.001)
            point_list.append(point)
    return point_list


# checkAdInsertion("121.382 31.232")

time_start = time.time()

point_list = generatePoint()
err_count = 0

for point in point_list:
    print(point)
    if not checkAdInsertion(point):
        err_count = err_count + 1
print point_list
print "err_count===>" + str(err_count)
time_end = time.time()
print 'totally cost' + str(time_end - time_start)
