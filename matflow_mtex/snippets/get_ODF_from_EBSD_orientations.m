function ODF = get_ODF_from_EBSD_orientations(EBSD_orientations, specimenSym)
    EBSD_orientations.SS = specimenSymmetry(specimenSym);
    ODF = calcDensity(EBSD_orientations);
end
