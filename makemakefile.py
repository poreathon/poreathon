import glob
import yaml

pipelines = yaml.load(file('pipelines.yaml'))
recipes = glob.glob('recipes/*.yaml')
recipes = dict([(r[8:-5], yaml.load(file(r))) for r in recipes])

for pipeline, inputs in pipelines.iteritems():
	for input_file in inputs:
		for recipe_name, recipe_info in recipes.iteritems():
			if recipe_info['type'] == pipeline:
				if recipe_info['input'] == 'fasta':
					suffix = 'fasta'
				elif recipe_info['input'] == 'fastq':
					suffix = 'fastq'
				else:
					raise SystemError("Wrong suffix name in YAML file %s" % (recipe_name))
					
				print "bpipe run -r -f %s_%s.html -d output/%s/%s -p ENTRYPOINT=recipes/%s.pipe @params.txt pipelines/%s.pipe input/nanopore/%s.%s" % (recipe_name, input_file, pipeline, recipe_name, recipe_name, pipeline, input_file, suffix)



