import heapq

heap = []

trans = {"who":1, "quantity":-3}
heapq.heappush(heap, (-3, id(trans), trans))
trans = {"who":3, "quantity":5}
heapq.heappush(heap, (-3, id(trans), trans))
trans = {"who":2, "quantity":2}
heapq.heappush(heap, (-2, id(trans), trans))

print(len(heap))
while heap:
    allocation = heapq.heappop(heap)[2]
    print(str(allocation["quantity"]) + " to " + str(allocation["who"]))