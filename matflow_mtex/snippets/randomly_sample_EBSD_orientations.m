function orientations = randomly_sample_EBSD_orientations(EBSD_orientations, num_orientations)
    orientations = EBSD_orientations(randperm(EBSD_orientations.length, num_orientations));
end
