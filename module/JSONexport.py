import json

class JSONexport:
	log = [] # Storing JSONs

	def __init__(self):
		log = []

	# From filled Concept to JSON export and save as file
	def export(self, concept):
		f = open("result/export.json", 'w', encoding = 'utf-8')
		overall = dict()
		context = []
		elem = dict()
		elem['service'] = concept.getName()
		fields = []
		for field in concept.getFields():
			fields.append(self.fieldToDict(concept.getName(), field))
		elem['fields'] = fields
		context.append(elem)
		overall['context'] = context
		f.write(json.dumps(overall, indent=2))
		f.close()

	def fieldToDict(self, name, field):
		elem = dict()
		elem['field_name'] = name + ':' + field.getName()
		elem['field_type'] = field.getType()
		elem['field_value'] = field.getValue()
		elem['field_priority'] = field.getPriority()
		return elem