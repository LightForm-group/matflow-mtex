function ODF = get_random_ODF(crystalSym, specimenSym, numOrientations)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);
    ori = orientation.rand(numOrientations, crystalSym, specimenSym);
    ODF = calcDensity(ori);
end
