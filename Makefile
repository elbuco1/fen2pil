.PHONY: clean data lint requirements

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
# BUCKET = [OPTIONAL] your-bucket-for-syncing-data (do not include 's3://')
# PROFILE = default
PROJECT_NAME = fen2pil
PYTHON_INTERPRETER = python3
PACKAGE_NAME =  fen2pil

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

ENV_FILE = environment.yml

#################################################################################
# COMMANDS                                                                      #
#################################################################################

#################################################################################
# Requirements                                                                  #
#################################################################################
## Install local code as package
install_package_dev: test_environment
	conda env update --file $(ENV_FILE)

	$(PYTHON_INTERPRETER) -m pip install -e .


install_package: test_environment
	$(PYTHON_INTERPRETER) -m pip install .

## Uninstall local code package
uninstall_package: 
	# uninstall
	$(PYTHON_INTERPRETER) -m pip uninstall $(PACKAGE_NAME)
	rm -r $(PACKAGE_NAME).egg-info

## Create conda environment from environment.yml file
create_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
		conda env create -f $(ENV_FILE)
		@echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
endif

## Update conda environment from environment.yml file
update_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, updating conda environment."
		# conda env update --prefix ./env --file environment.yml  --prune
		conda env update -f environment.yml -n $(PROJECT_NAME)
		@echo ">>> Conda env updated. Activate with:\nconda activate $(PROJECT_NAME)"
endif

## Delete conda environment
remove_environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, removing conda environment"
		conda remove --name $(PROJECT_NAME) --all
endif

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py


## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
