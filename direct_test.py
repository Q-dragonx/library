# 直接测试借书业务逻辑
from datetime import datetime, timedelta

# 模拟库存检查函数
def check_borrow_availability(stock):
    """检查图书是否可借"""
    if stock <= 0:
        return "库存不足"
    return "可以借书"

# 测试库存为0的情况
print("测试用例TC-001：库存为0时借书")
print("输入：bookId=1001, stock=0")

# 执行测试
result = check_borrow_availability(0)
print(f"预期输出：返回'库存不足'")
print(f"实际输出：{result}")

# 检查结果
if result == "库存不足":
    print("测试结果：通过")
else:
    print("测试结果：失败")

# 再测试库存大于0的情况
print("\n测试库存充足的情况")
print("输入：bookId=1002, stock=5")

result2 = check_borrow_availability(5)
print(f"预期输出：返回'可以借书'")
print(f"实际输出：{result2}")

if result2 == "可以借书":
    print("测试结果：通过")
else:
    print("测试结果：失败")