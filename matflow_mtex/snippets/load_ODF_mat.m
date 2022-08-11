function ODF = load_ODF_mat(ODF_mat_path, crystalSym, specimenSym)
    crystalSym = crystalSymmetry(crystalSym);
    specimenSym = specimenSymmetry(specimenSym);
    ODF_struct = load(ODF_mat_path);
    ODF = ODF_struct.odf;
end
