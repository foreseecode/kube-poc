import groovy.yaml.YamlSlurper
import groovy.yaml.YamlBuilder

if(args.length != 2) {
  println "Not enough parameters. 2 expected"
  return
}

def pop = args[0]
def value = args[1]
def file_name = 'values.yaml'
def obj = new YamlSlurper().parse(new File(file_name))

obj.get("image").get("tag").put(pop, value)

def yaml = new YamlBuilder()
yaml(obj)
new File(file_name).write(yaml.toString())
