face-in-picture-classifier
==========================

Software to determine what important metrics might be for the sale of a product.

Project components:

- Scrapper using the Etsy API to extract tags and images associated with listings
- Facial recognition software to detect faces in listing images
  - Haar classifier testing suite to determine the best classifier to use
    for a given data set
- Tag clustering software, to determine which tags appear frequently together
  for the purposes of creating a feature vector
  - Depth first search to determine connected components
- SVM and pegasos classifiers to check relevance of listing features
 