-- Manual garbage collection interface example
data = {"trash1", "trash2", "trash3", "trash4"}

-- Returns the amount of memory currently used by the program in kilobytes.
print(collectgarbage("count"),"KB")

-- delete reference to trash table - actual data is still in memory
data = nil
print(collectgarbage("count"),"KB")

-- Run one complete cycle of garbage collection.
collectgarbage("collect")

-- After garbage collection pass
print(collectgarbage("count"),"KB")