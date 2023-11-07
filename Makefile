YAML_FILES = $(shell find src/yaml/ -type f -name '*.yaml')
GIF_FILES = $(patsubst src/yaml/%.yaml, src/yaml/%.gif, $(YAML_FILES))

.PHONY: all
all: $(GIF_FILES)

%.gif: __main__.py %.yaml
	pipenv run python $^
