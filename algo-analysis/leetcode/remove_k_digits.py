class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        if len(num) == k:
            return "0"

        stack = []
        for digit in num:
            while k > 0 and stack and stack[-1] > digit:
                stack.pop()
                k -= 1
            stack.append(digit)

        stack = stack[: len(stack) - k]
        while stack and stack[0] == "0":
            stack.pop(0)

        res = "".join(stack)
        return res if res else "0"
