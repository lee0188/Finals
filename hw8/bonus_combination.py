### HW08 Prob. 1
# bonus_combination.py
# Author: Ting-Kai Chang

### Problem description
# Xiao Ming cleared all levels in a show and got 
# different scores in different levels
# Finally, the host told him that he can arrange the scores 
# obtained in each level arbitrarily, and the combined number is the bonus he can get
# Help Xiao Ming earn the most bonus?

### Skills and functions
# range(), assignment,
# input(), print(), switch,
# int(), for loop, split()

### Example IO (cmd prompt: "DingKai > ")
# DingKai > python3 bonus_combination.py
# 87,23,46
# 874623
# DingKai > python3 bonus_combination.py
# 1
# 1
# DingKai > python3 bonus_combination.py
# 234,123,789,345
# 789345234123


### Reference solution
# different
# 處理輸入
nums = input().split(',')

# 雙層for迴圈去檢查哪個排前面比較大
for i in range(len(nums)-1):
    for j in range(len(nums)-(i+1)):
         # 如果換了比較大就換
        if int(nums[j+1] + nums[j]) > int(nums[j] + nums[j+1]):
            nums[j], nums[j+1] = nums[j+1], nums[j]

# 印出結果
for i in nums:
    print(i, end="")
