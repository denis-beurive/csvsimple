from csvsimple import Csv

# Define a formater that will be used to convert records into strings.

def myFormater(in_record, in_header):
	r = []
	for i in range(0, len(in_header)):
		name  = in_header[i]
		value = in_record[i]
		s     = "%s ===> %s" % (name.rjust(25), value)
		r.append(s)
	return "\n".join(r)

# Define matchers that will be used to select records.

def idMatcher(in_id):
	return in_id < 3

def firstNameMatcher(in_first_name):
	return in_first_name != 'toto4'

# Create a CSV container.
# This container defines 3 columns:
#     o id
#     o first name
#     o last name

header = ['id', 'first name', 'last name']
csv = Csv(header)

# Add records to the container.

csv.add([1, 'John', 'Carter'])
csv.add([2, 'John', 'Dupond'])
csv.add([3, 'John', 'XXXX'])

# Print all records, using the default formater.

print ("List of records in the container:")
print (csv)

# Print all records, using a specific formater.

csv.setFormater(myFormater)
print ("List of records in the container:")
print (csv)

# Select records using simple comparaison.

criterion = { 'first name': 'John' }
records = csv.select(criterion)
print ("First selection is:")
for r in records:
	print (myFormater(r, header))
	
criterion = { 'first name': 'John', 'id': 1 }
records = csv.select(criterion)
print ("Second selection is:")
for r in records:
	print (myFormater(r, header))

# Select records using pattern matching.

criterion = { 'first name': '^J', 'last name': '^(C|D)' }
records = csv.select(criterion, Csv.MATCH)
print ("Third selection is:")
for r in records:
	print (myFormater(r, header))
	
# Select records using functions.

criterion = { 'id': idMatcher, 'first name': firstNameMatcher }
records = csv.select(criterion, Csv.EXECUTE)
print ("Fourth selection is:")
for r in records:
	print (myFormater(r, header))

# Find out the number of records.

print ("The container contains %d records" % len(csv))

# Change the first record.

csv[0] = [10, 'Thomas', 'Cook']
print ("The first record has been changed:")
print (csv)

# Get the second record.

record = csv[1]
print ("This is the first record:")
print (myFormater(record, header))

# Get a record's value by name.

print ("Value 'id' of the second record is %d." % csv.getValue(csv[1], 'id'))

# Get all the columns' names.

print ("CSV's columns:")
for name in csv.keys():
	print ("    - %s" % name)

# Get all values for each columns.

print ("Values per columns:")
for name, value in csv.items():
	print ("    - %s: %s" % (name, value))

# Get values (columns's names are omited).

print ("Values per columns (columns's names are omited):")	
for value in csv.values():
	print ("    - %s" % value)
	
# Remove a record.

del csv[0]
print ("The first record has been removed:")
print (csv)

# Clear the container.

csv.void()
