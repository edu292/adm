class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
        if head is None or head.next is None:
            return head

        node = head.next.next
        len = 2
        while node is not None:
            node = node.next
            len += 1

        shift = k % len
        if shift == 0:
            return head

        new_tail_index = (len - 1) - shift
        new_tail = head
        for i in range(new_tail_index):
            new_tail = new_tail.next

        new_head = new_tail.next
        new_tail.next = None

        splice_node = new_head
        for i in range(shift - 1):
            splice_node = splice_node.next

        splice_node.next = head

        return new_head
