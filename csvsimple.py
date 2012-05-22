## @package base
#  This file contains the implementation of the basic CSV class.

import re
import collections
import sys

if sys.version_info < (3, 0):
    raise RuntimeError("Module CSV requires Python 3.0 or greater!")

__all__ = ['Csv']


## This class handles CSV data. 
#
#  This class "partially" implements the following interfaces:
#  <ul>
#     <li>Sequence.</li>
#     <li>Mutable Mapping.</li>
#  </ul>
#
#  <pre>
#  <code>
#     csv = Csv(['id', 'first name', 'last name'])
#     csv.add([1, 'John', 'Carter'])
#     csv.add([2, 'John', 'Dupond'])
#     csv.add([3, 'John', 'XXXX'])
#     print ("%d" % len(csv))
#     record = csv[1]
#     del self.csv[1]
#
#     # Print all first names.
#     for record in csv: print (csv.getValue(record, 'first name'))
#
#     # Get all columns' names.
#     v = []
#     for c in csv.keys(): v.append(c)
#
#     # name: one column's name.
#     # value: all values for this column.
#     v = []
#     for name, value in csv.items(): v.append([name, value])
#
#     # v[0]: all value for column "id"
#     # v[1]: all value for column "first name"
#     # v[2]: all value for column "last name"
#     v = []
#     for value in csv.values(): v.append(value)
#  </code>
#  </pre>
#
#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples

class Csv:
	
	# -----------------------------------------------------------------
	# Class' methods.
	# -----------------------------------------------------------------
	
	## Default records' formater.
	#  @param in_record Record to convert into string.
	#  @param in_header List of columns' names that defines the CSV's structure.
	#  @return The method returns a string that represents the given record.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	@staticmethod
	def __formater(in_record, in_header):
		r = []
		for i in range(0, len(in_header)):
			name  = in_header[i]
			value = in_record[i]
			s     = "%s: %s" % (name.rjust(20), value)
			r.append(s)
		return "\n".join(r)
		
	
	## Return the default records' formater.
	#  @return The method returns the default records' formater.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	@staticmethod
	def getDefaultFormater():
		return Csv.__formater;
	
	# -----------------------------------------------------------------
	# Class' attributes.
	# -----------------------------------------------------------------

	## Triggers selection via simple equality. This value is used by the method select().	
	EQUALITY = 1
	## Triggers selection via pattern matching. This value is used by the method select().	
	MATCH    = 2
	## Triggers selection via function execution. This value is used by the method select().	
	EXECUTE  = 3
		
	# -----------------------------------------------------------------
	# Constructor.
	# -----------------------------------------------------------------

	## Create a CSV container.
	#  @param in_header This list contains the names of the columns that define the CSV structure.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def __init__(self, in_header):
		# Check for duplicated columns' names.
		c = collections.Counter(in_header)
		for column, count in c.items():
			if count > 1: raise RuntimeError('Duplicated columns "%s"!' % column)
			
		# Create instance's attributes.
		self.__positions = {}                           # Association between columns' names and values' positions.
		self.__header    = in_header                    # Names of columns.
		self.__count     = len(in_header)               # Number of columns.
		self.__records   = []                           # List of list.
		self.__index     = 0                            # Used for the iterator.
		self.__format    = Csv.getDefaultFormat()	    # Default values for string conversion.

		# Build the association between columns' names and values' positions.
		pos = 0		
		for name in in_header:
			self.__positions[name] = pos
			pos += 1

	# -----------------------------------------------------------------
	# Public instance's methods.
	# -----------------------------------------------------------------

	## Add a record to the CSV container.
	#  @param in_record This list contains the values to add.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def add(self, in_record):
		# Make sure that the number of values is correct.
		if not len(in_record) == self.__count: raise RuntimeError('Invalid number of values for record (found %d, expected %d)' % (len(in_record), self.__count))
		self.__records.append(in_record)

	## Clear the CVS container.	
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def void(self): self.__records = []


	## Select records fro the CSV container.
	#  @param in_criterias This dictionary contains selections' criterions.
	#         <ul>
	#             <li>Dictionary's key : the name of a column.</li>
	#             <li>Dictionary's value: this value can be : a simple value, a regular expression or a functioin.
	#                 The type of value depends on the value of parameter "in_action".</li>
	#         </ul>
	#         If this parameter is not specified, then the method returns all the records in the container.
	#  @param in_action This parameter defines the selection's method. 
	#         Three methods are available :
	#         <ul>
	#             <li>Csv.EQUALITY (1): Simple equality.
	#                 Dictionary's values must be simple values.</li>
	#             <li>Csv.MATCH (2): Pattern matching.
	#                 Dictionary's values must be regular expressions.</li>
	#             <li>Csv.EXECUTE (3): Execution of code.
	#                 Dictionary's values must be functions.
	#                 Function's signature is: def myFuntion(in_value)</li>
	#         </ul>
	#  @return The method returns a lust of records.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def select(self, in_criterias=None, in_action=1):
		if in_criterias is None: return self.__records;
		res = []
		for record in self.__records:
			r = True
			for key, value in in_criterias.items():
				if not key in self.__header: raise RuntimeError('Unexpected name (%s) for criteria!' % key)
				record_value = record[self.__position(key)]
				
				# Simple comparaison.
				if in_action == Csv.EQUALITY:
					if not value == record_value:
						r = False
						break
				else:
					# Matching.
					if in_action == Csv.MATCH:
						reg = re.compile(value)
						if not re.match(reg, record_value):
							r = False
							break
					else:
						# Verify through function's execution.
						if in_action == Csv.EXECUTE:
							if not value(record_value):
								r = False
								break
						else:
							raise RuntimeError('Invalid select method (%d)!' % in_action)
			if r: res.append(record)
		return res

	## Set a function used to print records.
	#  @param in_formatter Function with the following signature: def myFunction(in_record, in_header)
	#         This function must return a string.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def setFormater(self, in_formatter):
		self.__format = in_formatter
	
	## Return the function used to print records.
	#  @return Te method returns the function used to print records.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples	
	def getFormater(self):
		return self.__format

	## This method returns a list of strings. Each string represents a record.
	#  @return The method returns a list of strings. Each string represents a record.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def strs(self):
		result = []
		for record in self.__records:
			# print ("==> %s" % self.__format(record, self.__header))
			result.append(self.__format(record, self.__header))
		return result
	
	## Get the value of a given column, for a given record.
	#  @param in_record The record.
	#  @param in_column_name Name of the column.
	#  @return The method returns the value for the given column.
	#  @remark See example on https://github.com/denis-beurive/csvsimple/tree/master/examples
	def getValue(self, in_record, in_column_name):
		return in_record[self.__position(in_column_name)]
		
	# -----------------------------------------------------------------
	# Sequence's interface.
	# -----------------------------------------------------------------
				
	def __iter__(self): return self

	def __next__(self):
		if self.__index < len(self.__records):
			self.__index += 1
			return self.__records[self.__index-1]
		else:
			self.__index = 0
			raise StopIteration

	def __len__(self): return len(self.__records)
	
	def __getitem__(self, in_index):
		return self.__records[in_index]
	
	def __setitem__(self, in_index, in_value):
		self.__records[in_index] = in_value	
	
	def __delitem__(self, in_index):
		del self.__records[in_index]

	# -----------------------------------------------------------------
	# Mapping's interface
	# -----------------------------------------------------------------

	def keys(self):
		return self.__header
	
	def items(self):
		v = []
		for name in self.__header:
			r = []
			for record in self.__records: r.append(record[self.__position(name)])
			v.append([name, r])
		return v	
			
	def values(self):
		v = []
		for name in self.__header:
			r = []
			for record in self.__records: r.append(record[self.__position(name)])
			v.append(r)
		return v	

	# -----------------------------------------------------------------
	# Other methods
	# -----------------------------------------------------------------

	def __str__(self):
		return "\n".join(self.strs())

	# -----------------------------------------------------------------
	# Private instance's methods.
	# -----------------------------------------------------------------

	def __position(self, in_name):		
		return self.__positions[in_name]
	

