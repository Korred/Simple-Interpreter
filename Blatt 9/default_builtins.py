# things to change - 

builtin = """
object inttrait:
	def add(x):
		self $int_add(x)

	def sub(x):
		self $int_sub(x)

	def mul(x):
		self $int_mul(x)

	def div(x):
		self $int_div(x)

object floattrait:
	def add(x):
		self $float_add(x)

	def sub(x):
		self $float_sub(x)

	def mul(x):
		self $float_mul(x)

	def div(x):
		self $float_div(x)

object listtrait:
	def add(x):
		self $list_add(x)

	def del(x):
		self $list_del(x)

	def get(x):
		self $list_get(x)

	def len:
		self $list_len

	def append(x):
		l = x len
		while l:
			c = x get(0)
			self add(c)
			l = l sub(1)


def to_int(x):
	$to_int(x)

def to_float(x):
	$to_float(x)

def to_str(x):
	$to_str(x) 

def ceil(x):
	$ceil(x)

def floor(x):
	$floor(x)

"""