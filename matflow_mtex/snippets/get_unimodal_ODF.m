function ODF = get_unimodal_ODF(crystalSym, specimenSym, modalOrientation, halfwidth)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);
    ori = orientation('Euler', modalOrientation*degree, crystalSym, specimenSym);
    ODF = unimodalODF(ori, 'halfwidth', halfwidth*degree);
end
