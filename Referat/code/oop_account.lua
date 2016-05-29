Account = {balance = 0}

-- same as Account.new(self,o)
function Account:new (o) -- __init__ in python
  o = o or {}   -- create object if user does not provide one
  setmetatable(o, { __index = self })
  return o
end

-- same as Account.withdraw(self,v)
function Account:withdraw (v)
  print("Withdrawing:",v)
  self.balance = self.balance - v
end

function Account:deposit (v)
  print("Depositing:",v)
  self.balance = self.balance + v
end

SpecialAccount = Account:new() -- instance of Account
    
acc1 = Account:new()
acc2 = Account:new()
s_acc = SpecialAccount:new({limit=1000})
print("Account1 - Current balance:",acc1.balance)
print("Account2 - Current balance:",acc2.balance)
print("Special Account - Current balance:",s_acc.balance)
print("Special Account - Limit:",s_acc.limit,"\n")

acc1:deposit(20)
acc2:withdraw(20)

print()
print("Account1 - Current balance:",acc1.balance)
print("Account2 - Current balance:",acc2.balance)



