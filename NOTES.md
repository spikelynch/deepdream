Notes for improvements
======================

Command line arguments to dream.py

- iter_n = number of iterations
- octaves = number of octaves
- model = specify a model    - check that the model exists
- layer = specify a layer    - check if the model provides it

For the future: a specfile which gives a recipe like:

- iterate 5 x model1:layer1
- iterate 100 x model1:layer2


Good combinations

Lots of eyes

/dream.py --guide Input/Cells3.jpg --guidelayer inception_3b/3x3_reduce Input/red_rock.jpg
