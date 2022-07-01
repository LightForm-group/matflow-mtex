function ODF = load_ODF_mat(ODF_mat_path, crystalSym, specimenSym)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);    
    ODF = load(ODF_mat_path)
    );
end
