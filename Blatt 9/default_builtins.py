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