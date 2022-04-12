import random

def monotoneStack(nums):
	print(nums)
	stack = []
	for num in nums:
		while stack and num <= stack[-1]:
			top = stack[-1]
			stack.pop()
			print(f"{str(top)} 出栈 {stack}")
		stack.append(num)
		print(f"{str(num)} 入栈 {stack}")
		
def monotoneIncreasingStack(nums):
	stack = []
	for num in nums:
		while stack and num >= stack[-1]:
			top = stack[-1]
			stack.pop()
			print(f"{str(top)} 出栈 {stack}")
		stack.append(num)
		print(f"{str(num)} 入栈 {stack}")
		
def monotoneDecreasingStack(nums):
	stack = []
	for num in nums:
		while stack and num <= stack[-1]:
			top = stack[-1]
			stack.pop()
			print(f"{str(top)} 出栈 {stack}")
		stack.append(num)
		print(f"{str(num)} 入栈 {stack}")
		

nums = [random.randint(1, 9) for _ in range(8)]
print(nums)
#nums = [4, 3, 2, 5, 7, 4, 6, 8]
monotoneIncreasingStack(nums)