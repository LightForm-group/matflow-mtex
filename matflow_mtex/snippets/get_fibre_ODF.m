function ODF = get_fibre_ODF(crystalSym, specimenSym, halfwidth)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);
    psi = deLaValleePoussinKernel('halfwidth', halfwidth*degree);
    f = fibre.beta(crystalSym, specimenSym);
    ODF = fibreODF(f, psi);
end
