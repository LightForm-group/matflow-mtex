function orientations = randomly_sample_EBSD_orientations(EBSD_orientations, numOrientations)
    orientations = EBSD_orientations(randperm(EBSD_orientations.length, numOrientations));
end
