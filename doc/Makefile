clean:
	rm -rf build

html:
	sphinx-build -b html . build/html

readme:
	sphinx-build -b rst . build/rst
	cp build/rst/index.rst ../README.rst