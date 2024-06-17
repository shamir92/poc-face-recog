PHONY: start/pocv2
start/pocv2:
	rm -rf ./output/pocv2/predict
	python ./process/poc-v2.py