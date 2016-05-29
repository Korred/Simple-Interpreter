-- example shows dynamic typing and introspection

-- 6/8 lua types - number, string, table, function, boolean, nil
a = 1 
print("a", a, type(a))

a = "Hello!" 
print("a", a, type(a))

a = {1, "a", 1.2}
print("a", a, type(a))

a = print
print("a", a, type(a))

a = true
print("a", a, type(a))

a = nil
print("a", a, type(a))
