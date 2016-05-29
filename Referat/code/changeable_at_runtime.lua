-- example showing the MOST THINGS CHANGEABLE AT RUN-TIME property using
-- metatables and metamethodes

-- Example 1
print("Example1: __index metamethod\n")
main_table = { key1 = 1337 }
meta_table = { key1 = 123, key2 = 42 } 

print("Results without metatable:")
print("key1", main_table.key1)
print("key2", main_table.key2)
print()

-- set metatable using metamethod __index as fallback
-- if key not in main_table look in meta_table next
setmetatable(main_table, {__index = meta_table})

print("Results with metatable and __index metamethod:")
print("key1", main_table.key1)
print("key2", main_table.key2)

setmetatable(main_table, {
   __index = function(mytable, key)
		return 666
   end
})

print("\nResults with metatable and different __index metamethod:")
print("key1", main_table.key1)
print("key2", main_table.key2)


-- Example 2
print("\n\nExample2: __add (UNION) metamethod\n")
table1 = {1,1,1,1}
table2 = {9,9,9,9}

--__add used define behavior of + operator.
print("{1,1,1,1}+{9,9,9,9} ?")
print("PLUS(+)-operator behavior can be changed at runtime!!\n")
setmetatable(table1, {
   __add = function(op1,op2)
      return "no useful data"
   end
})

print("Plus operator returns no useful data: ")
print(table1+table2)


setmetatable(table1, {
   __add = function(op1, op2)
   		sum = 0
   		for k,v in ipairs(op1) do
   			sum = sum + v
   		end
   		for k,v in ipairs(op2) do
   			sum = sum + v
   		end
      return sum
   end
})
print()
print("Plus operator returns sum of all entries: ")
print(table1+table2)

setmetatable(table1,{
   __add = function(op1, op2)
	
      for i = 1, table.maxn(op2) do
         table.insert(op1, table.maxn(op1)+1,op2[i])
      end
      return op1
   end
})
print()
print("Plus operator returns concat of entries: ")
concat = table1+table2
str = ""
for k,v in ipairs(concat) do
	if k == 1 
	then
		str = str..v
	else
		str = str..", "..v
	end
end
print(str)
