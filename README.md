# bilayer-graphene

Latest commit changes: In this latest commit, I resolved the temperature issue, where it wouldn't level off at the desired temperature before the equilibration phase ends. I made the following changes:

1) Increased distance between Fluorine regions and graphene sheets
2) Changed the damping parameter for the NVT runs so that temperature adjustments are more frequent, to mitigate overshooting
3) Added a minimization step before the NVT runs in the equilibration stage