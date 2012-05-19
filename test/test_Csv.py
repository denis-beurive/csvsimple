import unittest
from csvsimple import Csv #@UnresolvedImport

# -----------------------------------------------------------------
# Some function that will be used to test the selection by
# functions' execution.
# -----------------------------------------------------------------

def idMatcher(in_id):
	return in_id < 3
	
def firstNameMatcher(in_first_name):
	return in_first_name != 'toto4'
	
def formater(in_record, in_header):
	r = []
	for i in range(0, len(in_header)):
		name  = in_header[i]
		value = in_record[i]
		s     = "%s: %s" % (name.rjust(20), value)
		r.append(s)
	return "\n".join(r)

# -----------------------------------------------------------------
# Test cases.
# -----------------------------------------------------------------

class TestCsv(unittest.TestCase):
	
	def setUp(self):
		self.csv = Csv(['id', 'first name', 'last name'])
		self.csv.add([1, 'John', 'Carter'])
		self.csv.add([2, 'John', 'Dupond'])

	def test_select_equality(self):
		records = self.csv.select({'id': 1, 'first name': 'John'}, Csv.EQUALITY)
		self.assertTrue(len(records) == 1)
		records = self.csv.select({'first name': 'John'}, Csv.EQUALITY)
		self.assertTrue(len(records) == 2)
		records = self.csv.select({'id': 3, 'first name': 'John'}, Csv.EQUALITY)
		self.assertTrue(len(records) == 0)
		
	def test_select_match(self):
		records = self.csv.select({'first name': '^J', 'last name': '^C'}, Csv.MATCH)
		self.assertTrue(len(records) == 1)
		records = self.csv.select({'first name': '^J', 'last name': '^(C|D)'}, Csv.MATCH)
		self.assertTrue(len(records) == 2)	
		records = self.csv.select({'first name': '^T', 'last name': '^(C|D)'}, Csv.MATCH)
		self.assertTrue(len(records) == 0)			
		
	def test_select_execute(self):
		records = self.csv.select({'id': idMatcher}, Csv.EXECUTE)
		self.assertTrue(len(records) == 2)
		records = self.csv.select({'id': idMatcher, 'first name': firstNameMatcher}, Csv.EXECUTE)
		self.assertTrue(len(records) == 2)

	def test_len(self):
		self.assertTrue(len(self.csv) == 2)
		
	def test_iterator(self):
		cpt = 0
		for i in self.csv:
			cpt += 1
		for i in self.csv:
			cpt += 1
		self.assertTrue(cpt == 2*len(self.csv))
		
	def test_getItem(self):
		record = self.csv[1]
		id = self.csv.getValue(record, 'id')
		self.assertTrue(id == 2)
		
	def test_delItmen(self):
		del self.csv[1]
		self.assertTrue(len(self.csv) == 1)
		record = self.csv[0]
		self.assertTrue(record[0] == 1)
		
	def test_setItem(self):
		self.csv[0] = [3, 'John', 'Dupond']
		record = self.csv[0]
		self.assertTrue(record[0] == 3)
		
	def test_keys(self):
		v = []
		for c in self.csv.keys(): v.append(c)
		self.assertTrue(v[0] == 'id')
		self.assertTrue(v[1] == 'first name')
		self.assertTrue(v[2] == 'last name')
		
	def test_items(self):
		v = []
		for name, value in self.csv.items(): v.append([name, value])
		self.assertTrue(v[0][0] == 'id')
		self.assertTrue(v[0][1][0] == 1)
		self.assertTrue(v[0][1][1] == 2)
		self.assertTrue(v[1][0] == 'first name')
		self.assertTrue(v[1][1][0] == 'John')
		self.assertTrue(v[1][1][1] == 'John')
		
	def test_values(self):
		v = []
		for value in self.csv.values(): v.append(value)
		self.assertTrue(v[0][0] == 1)
		self.assertTrue(v[0][1] == 2)
		self.assertTrue(v[1][0] == 'John')
		self.assertTrue(v[1][1] == 'John')
		
	def test_raise(self):
		self.assertRaises(RuntimeError, Csv, ['id', 'toto', 'toto'])
		self.assertRaises(RuntimeError, self.csv.add, [1,2,3,4])
		self.assertRaises(RuntimeError, self.csv.select, {'power':3})
		self.assertRaises(RuntimeError, self.csv.select, {'id':1}, 4)

	def test_str(self):
		self.csv.setFormater(formater)
		print (str(self.csv))

if __name__ == '__main__':
	unittest.main()
