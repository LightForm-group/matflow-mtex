function ODF = get_unimodal_ODF(crystalSym, specimenSym, modalOrientationHKL, modalOrientationUVW, halfwidth)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);
    psi = deLaValleePoussinKernel('halfwidth', halfwidth*degree);
    ori = orientation.byMiller(modalOrientationHKL, modalOrientationUVW, crystalSym, specimenSym);
    ODF = unimodalODF(ori, psi);
end
